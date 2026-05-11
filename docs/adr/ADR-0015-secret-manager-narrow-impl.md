# ADR-0015: Secret Manager Narrow Implementation Plan

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Limit the next implementation plan to schema, fixtures, and documentation boundaries only.

## Rejected Alternatives

- Implement keychain adapter now: rejected because it weakens boundaries, auditability, or Human final approval.
- Store secret references with local paths: rejected because it weakens boundaries, auditability, or Human final approval.
- Expand to wallet custody: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Narrow schema and fixture work may be mistaken for approval to implement custody behavior.
- Scope creep may add provider-specific fields before the secret manager boundary is finalized.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Keep implementation tasks limited to schemas, fixtures, and governance checks until Human approval changes scope.
- Recheck safe-config fields against PRODUCT_BOUNDARY.md before adding provider metadata.
- Review at phase gates; keep linked ledgers current.
