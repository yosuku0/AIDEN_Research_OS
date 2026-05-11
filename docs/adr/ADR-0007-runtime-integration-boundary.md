# ADR-0007: Runtime Integration Boundary

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Keep research artifacts above runtime execution and require reviewed artifacts plus Human gates.

## Rejected Alternatives

- Direct research-to-runtime handoff: rejected because it weakens boundaries, auditability, or Human final approval.
- AI-controlled release gate: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Research artifacts may be wired into runtime systems before a reviewed interface contract exists.
- Boundary bypass may occur if helper scripts are treated as deployment or production-write tooling.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Require a new ADR before any runtime interface, deployment target, or provider integration is introduced.
- Keep CI checks focused on governance artifacts until runtime boundary approval exists.
- Review at phase gates; keep linked ledgers current.
