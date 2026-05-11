# ADR-0003: Initial Monorepo Topology

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Use an initial monorepo for docs, governance, schemas, fixtures, tests, ledgers, tasks, and lab scaffolds.

## Rejected Alternatives

- Immediate multi-repo: rejected because it weakens boundaries, auditability, or Human final approval.
- Hybrid repo split before boundaries stabilize: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Premature repository splitting may break cross-ledger traceability between ADRs, tasks, schemas, and fixtures.
- Monorepo growth may blur ownership boundaries if package-level governance is not added before runtime work begins.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Reassess package ownership rules before adding implementation packages beyond governance scaffolding.
- Add topology notes to task templates when new top-level directories are proposed.
- Review at phase gates; keep linked ledgers current.
