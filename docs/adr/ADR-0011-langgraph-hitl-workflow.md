# ADR-0011: LangGraph HITL Workflow

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Use LangGraph StateGraph with checkpoints and interrupt-based Human approval gates.

## Rejected Alternatives

- Linear scripts: rejected because it weakens boundaries, auditability, or Human final approval.
- CrewAI as production orchestrator: rejected because it weakens boundaries, auditability, or Human final approval.
- Approval after execution: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Checkpoint persistence migration from in-memory to durable storage may lose approval state if migration is not versioned.
- LangGraph API changes may break interrupt-based HITL workflow compatibility.
- Timeout handling without durable checkpoint recovery may lose in-progress Human approval context.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Evaluate SQLite and Postgres checkpoint durability trade-offs before production readiness review.
- Track LangGraph changelog entries that affect `interrupt()` and checkpoint APIs.
- Define timeout duration policy for each restricted approval node type.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting follow-up rules.
