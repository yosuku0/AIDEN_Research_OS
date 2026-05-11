# ADR-0009: Research Lab Security Test Plan

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Adopt documentation-first security test specifications for governance, approval, secret handling, and execution isolation.

## Rejected Alternatives

- Executable tests before boundary approval: rejected because it weakens boundaries, auditability, or Human final approval.
- No test plan: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Documentation-only tests may create false assurance if no executable validation is introduced later.
- Unsafe fixtures may accidentally include credential-like literals if examples are not abstracted.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Migrate safe fixture validation through ADR-0018 without adding runtime behavior tests.
- Keep unsafe fixture examples structural and abstract, not credential-shaped.
- Review at phase gates; keep linked ledgers current.
