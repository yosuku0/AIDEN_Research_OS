# ADR-0004: Market Labs Directory Is labs

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Use labs/ for market-domain lab scaffolds.

## Rejected Alternatives

- Base-only root: rejected because it weakens boundaries, auditability, or Human final approval.
- Market-specific root repositories: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Lab artifacts may be mistaken for executable strategy or production configuration if labels are not explicit.
- Cross-lab comparisons may become inconsistent without common fixture and evidence conventions.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Add lab artifact examples only when they include clear non-execution boundary language.
- Align future lab evidence files with research-ledger and redaction checklist requirements.
- Review at phase gates; keep linked ledgers current.
