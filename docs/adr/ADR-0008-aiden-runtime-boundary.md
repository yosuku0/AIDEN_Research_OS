# ADR-0008: AIDEN Runtime Boundary

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Define AIDEN as orchestrator and runtime substrate, not signer, deployer, or execution authority.

## Rejected Alternatives

- AIDEN as autonomous executor: rejected because it weakens boundaries, auditability, or Human final approval.
- AIDEN as credential custodian: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Orchestrator language may expand into implied custody or execution authority if action verbs are not constrained.
- Future adapter work may tempt direct credential retrieval before approval records and tests are in place.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Audit new orchestration docs for signing, transfer, deploy, and production-write language.
- Link future adapter tasks back to approval records before implementation scaffolds are added.
- Review at phase gates; keep linked ledgers current.
