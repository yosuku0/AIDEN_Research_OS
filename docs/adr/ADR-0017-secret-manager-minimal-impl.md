# ADR-0017: Secret Manager Minimal Implementation

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Permit only safe config schema, no-secret fixtures, and documentation-only checks.

## Rejected Alternatives

- Secret manager runtime: rejected because it weakens boundaries, auditability, or Human final approval.
- Credential rotation implementation: rejected because it weakens boundaries, auditability, or Human final approval.
- CI enforcement in this phase: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Schema-only validation may create an illusion of security if CI does not reject unsafe fixture shapes.
- Minimal fixtures may miss edge cases around reference IDs, incident blockers, and approval references.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Add executable schema validation for safe and unsafe fixtures through ADR-0018.
- Expand fixture coverage only with abstract markers and no credential-like values.
- Review at phase gates; keep linked ledgers current.
