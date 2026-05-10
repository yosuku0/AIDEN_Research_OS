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

Documentation may drift, approval semantics may become ambiguous, and future contributors may confuse market lab scaffolds with execution systems.

## Follow-ups

Review this ADR at phase gates, keep linked ledgers current, and open follow-up tasks only within approved boundaries.
