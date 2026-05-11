# ADR-0006: Governance Ledger Schema

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Standardize ledger schemas for decisions, risks, approvals, redaction, incidents, task promotion, open questions, and phase gates.

## Rejected Alternatives

- Free-form notes: rejected because it weakens boundaries, auditability, or Human final approval.
- Issue-only governance: rejected because it weakens boundaries, auditability, or Human final approval.
- Runtime logs as ledgers: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Ledger tables may drift from JSON schemas if structure validation is not kept in CI.
- Strict schemas may block legitimate governance metadata unless extension policy is defined before new fields are introduced.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Keep ledger validation rules synchronized with docs/governance/LEDGER_SCHEMA.md.
- Track schema extension requests through SCHEMA_EVOLUTION_POLICY.md before adding new ledger fields.
- Review at phase gates; keep linked ledgers current.
