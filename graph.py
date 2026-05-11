"""
aiden.workflow.graph
~~~~~~~~~~~~~~~~~~~~
LangGraph StateGraph with Human-in-the-Loop (HITL) interrupt gates.

Implements ADR-0011, LANGGRAPH_WORKFLOW.md, and TECH_STACK_MATRIX.md:
  - Max 15 steps per workflow
  - Circuit breaker: SHA-256 hash comparison over last N turns
  - Checkpoint: InMemoryCheckpointer (SQLite path prepared for production)
  - HITL: interrupt() before any restricted decision
  - Session cost and token tracking (resolves audit HIGH-03)
  - Audit event emission on every state transition
"""

from __future__ import annotations

import hashlib
import json
from typing import Annotated, Any, TypedDict

import structlog
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import interrupt

from aiden.config.settings import AidenSettings, get_settings
from aiden.observability.tracer import AuditEvent, emit_audit_event

log = structlog.get_logger(__name__)

# ── Restricted decision types that require Human interrupt ───────────────────
HUMAN_GATE_TRIGGERS = frozenset({
    "merge",
    "capital",
    "allowlist_change",
    "release",
    "phase_gate",
    "hard_ban_change",
    "authority_change",
    "secret_registration",
})


# ── State schema ─────────────────────────────────────────────────────────────

class ResearchState(TypedDict):
    """
    Immutable-ish workflow state carried between LangGraph nodes.
    session_cost_usd and session_tokens enforce budget caps (audit HIGH-03).
    """

    messages: Annotated[list[BaseMessage], add_messages]
    step_count: int
    session_tokens: int
    session_cost_usd: float         # Tracks cumulative spend; enforced by router
    approval_required: bool
    approval_type: str              # One of HUMAN_GATE_TRIGGERS or ""
    current_phase: str
    trace_id: str
    actor: str
    governance_policy: str
    circuit_breaker_hashes: list[str]   # Rolling hash window for loop detection
    last_interrupt_reason: str


# ── Node implementations ──────────────────────────────────────────────────────

def _hash_messages(messages: list[BaseMessage]) -> str:
    """SHA-256 of the last message content. Used for circuit breaker."""
    if not messages:
        return ""
    last = messages[-1]
    content = last.content if isinstance(last.content, str) else json.dumps(last.content)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def research_node(state: ResearchState, *, settings: AidenSettings | None = None) -> dict[str, Any]:
    """
    Main research processing node.
    Emits an audit event and enforces step + budget limits.
    """
    cfg = settings or get_settings()
    step = state["step_count"] + 1

    # ── Hard step cap ────────────────────────────────────────────────────────
    if step > cfg.max_steps:
        emit_audit_event(AuditEvent(
            trace_id=state["trace_id"],
            actor=state["actor"],
            event="workflow.step_cap_exceeded",
            governance_policy="TECH_STACK_MATRIX.max_steps",
            result="stopped",
        ))
        return {"step_count": step, "approval_required": True, "approval_type": "phase_gate"}

    # ── Budget soft guard (hard guard is in the router) ──────────────────────
    if state["session_cost_usd"] >= cfg.budget_usd:
        emit_audit_event(AuditEvent(
            trace_id=state["trace_id"],
            actor=state["actor"],
            event="workflow.budget_exceeded",
            governance_policy="MODEL_ROUTING_COST_LIMITS.budget_usd",
            result="stopped",
        ))
        return {"step_count": step, "approval_required": True, "approval_type": "capital"}

    # ── Circuit breaker ──────────────────────────────────────────────────────
    new_hash = _hash_messages(state["messages"])
    hashes = state["circuit_breaker_hashes"][-cfg.circuit_breaker_turns:]
    if len(hashes) >= cfg.circuit_breaker_turns and all(h == new_hash for h in hashes):
        log.warning(
            "circuit_breaker.triggered",
            trace_id=state["trace_id"],
            hash=new_hash,
            turns=cfg.circuit_breaker_turns,
        )
        emit_audit_event(AuditEvent(
            trace_id=state["trace_id"],
            actor=state["actor"],
            event="workflow.circuit_breaker_triggered",
            governance_policy="TECH_STACK_MATRIX.circuit_breaker",
            result="stopped",
        ))
        return {
            "step_count": step,
            "approval_required": True,
            "approval_type": "phase_gate",
            "circuit_breaker_hashes": hashes + [new_hash],
        }

    emit_audit_event(AuditEvent(
        trace_id=state["trace_id"],
        actor=state["actor"],
        event=f"workflow.step.{step}",
        governance_policy=state["governance_policy"],
        result="processing",
    ))

    return {
        "step_count": step,
        "circuit_breaker_hashes": (hashes + [new_hash])[-cfg.circuit_breaker_turns:],
    }


def hitl_gate_node(state: ResearchState) -> dict[str, Any]:
    """
    Human-in-the-Loop gate node.
    Calls interrupt() to pause the workflow until a human provides approval.

    The approval_type must be one of HUMAN_GATE_TRIGGERS.
    AI agents cannot satisfy this gate — they are not valid approvers.
    """
    approval_type = state.get("approval_type", "unknown")

    emit_audit_event(AuditEvent(
        trace_id=state["trace_id"],
        actor=state["actor"],
        event="workflow.hitl_gate.requested",
        governance_policy="ADR-0011.hitl_interrupt",
        result=f"interrupt_pending:{approval_type}",
    ))

    log.info(
        "hitl_gate.interrupt",
        approval_type=approval_type,
        trace_id=state["trace_id"],
        message=(
            f"[HUMAN GATE] Workflow paused. "
            f"Approval type: '{approval_type}'. "
            f"See research/ledgers/approval-record.md to record your decision."
        ),
    )

    # LangGraph interrupt() suspends the graph here and serialises state to checkpoint.
    # Execution resumes when the graph is invoked again with the approval payload.
    human_response = interrupt({
        "approval_type": approval_type,
        "trace_id": state["trace_id"],
        "current_phase": state["current_phase"],
        "message": (
            f"Human approval required for '{approval_type}'. "
            f"Record decision in research/ledgers/approval-record.md, "
            f"then resume workflow."
        ),
    })

    # Validate that a human (not an AI) provided the response
    approver = human_response.get("approver", "") if isinstance(human_response, dict) else ""
    forbidden_approvers = {"AI", "Codex", "AIDEN", "codex", "aiden", "ai", "system"}
    if approver.strip() in forbidden_approvers:
        raise ValueError(
            f"Human gate cannot be satisfied by approver='{approver}'. "
            f"AI agents are not valid approvers. See EXECUTION_BOUNDARY.md."
        )

    emit_audit_event(AuditEvent(
        trace_id=state["trace_id"],
        actor=approver or "human_unknown",
        event="workflow.hitl_gate.approved",
        governance_policy="ADR-0011.hitl_interrupt",
        result="approved",
    ))

    return {
        "approval_required": False,
        "approval_type": "",
        "last_interrupt_reason": approval_type,
    }


# ── Routing logic ────────────────────────────────────────────────────────────

def route_after_research(state: ResearchState) -> str:
    """Route to HITL gate or END based on current state."""
    if state.get("approval_required"):
        return "hitl_gate"
    # Further routing logic can be added here (e.g. to model_router node)
    return END


# ── Graph builder ─────────────────────────────────────────────────────────────

def build_graph(
    checkpointer: object | None = None,
    settings: AidenSettings | None = None,
) -> StateGraph:
    """
    Build and compile the AIDEN research workflow graph.

    Args:
        checkpointer: LangGraph checkpointer instance. Defaults to MemorySaver.
                      For production, use SqliteSaver or AsyncPostgresSaver.
        settings:     AidenSettings instance. Defaults to module singleton.

    Returns:
        Compiled StateGraph ready for invocation.
    """
    cfg = settings or get_settings()
    cp = checkpointer or MemorySaver()

    builder = StateGraph(ResearchState)

    # Nodes
    builder.add_node("research", lambda s: research_node(s, settings=cfg))
    builder.add_node("hitl_gate", hitl_gate_node)

    # Edges
    builder.add_edge(START, "research")
    builder.add_conditional_edges("research", route_after_research)
    builder.add_edge("hitl_gate", "research")   # Resume research after gate is cleared

    return builder.compile(checkpointer=cp, interrupt_before=["hitl_gate"])


def make_initial_state(
    *,
    trace_id: str,
    actor: str,
    phase: str,
    governance_policy: str = "PRODUCT_BOUNDARY",
) -> ResearchState:
    """Factory for a well-formed initial ResearchState."""
    return ResearchState(
        messages=[],
        step_count=0,
        session_tokens=0,
        session_cost_usd=0.0,
        approval_required=False,
        approval_type="",
        current_phase=phase,
        trace_id=trace_id,
        actor=actor,
        governance_policy=governance_policy,
        circuit_breaker_hashes=[],
        last_interrupt_reason="",
    )
