# LANGGRAPH_WORKFLOW

## Purpose

Design LangGraph workflows with checkpoint persistence and Human-in-the-Loop approval gates.

## StateGraph Design

LangGraph StateGraph is the primary orchestration design. The graph contains Supervisor, MarketAnalyst, Coder, Reviewer, and HumanApproval nodes.

## Checkpoint Persistence

Checkpoint persistence starts with InMemory for prototypes, progresses to SQLite for local durability, and moves to Postgres or PostgresSaver for production readiness after Human approval.

## Interrupt Patterns

Use interrupt_before before restricted decisions such as merge, release, allowlist, capital, phase gate, and authority changes. Use interrupt_after for post-review audit capture and knowledge updates.

## Conditional Edges

Approve continues within scope. Edit routes back to the responsible node. Reject stops or returns to planning. Hold pauses until blockers are resolved.

## Durable Execution Modes

Durable execution design supports sync, async, and exit modes. All modes must preserve auditability, replay safety, and Human approval state.


## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md, research/ledgers/approval-record.md.
