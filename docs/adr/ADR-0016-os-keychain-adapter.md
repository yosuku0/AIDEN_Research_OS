# ADR-0016: OS Keychain Adapter Boundary

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Define a future adapter boundary limited to metadata-only behavior until separately approved.

## Rejected Alternatives

- Secret retrieval adapter: rejected because it weakens boundaries, auditability, or Human final approval.
- Secret storage adapter: rejected because it weakens boundaries, auditability, or Human final approval.
- Key generation adapter: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Adapter scope may drift from metadata reference handling into secret retrieval or storage without approval.
- Platform keychain differences may hide failure modes that fake tests do not catch.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Require fake-keyring tests before enabling any OS-specific backend behavior.
- Validate reference-id-only constraints against safe-config schema before adapter methods are added.
- Review at phase gates; keep linked ledgers current.
