# ADR-0002: GitHub Is Source of Truth

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Use GitHub reviewed artifacts as the canonical source of truth, supported by protected branches, CODEOWNERS, issue forms, and workflow files.

## Rejected Alternatives

- Local folders as canonical: rejected because it weakens boundaries, auditability, or Human final approval.
- Chat transcripts as canonical: rejected because it weakens boundaries, auditability, or Human final approval.
- Knowledge app as canonical: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Offline or local-only artifacts may diverge from reviewed GitHub records and bypass ledger traceability.
- Misconfigured CODEOWNERS may allow governance changes without the intended Human review path.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Verify CODEOWNERS coverage before any phase gate is considered ready for merge.
- Keep raw local artifacts out of GitHub and promote only reviewed summaries into ledgers.
- Review at phase gates; keep linked ledgers current.
