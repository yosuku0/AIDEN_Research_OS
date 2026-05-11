# ADR-0012: Local Storage Credential Rotation

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Keep raw artifacts local-only and define rotation SOP boundaries.

## Rejected Alternatives

- Raw artifacts in GitHub: rejected because it weakens boundaries, auditability, or Human final approval.
- Permanent local retention: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Raw local artifacts may persist beyond retention policy if purge steps are not operationally checked.
- Rotation evidence may expose local path details if redaction rules are not followed.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Add retention verification to redaction checklist updates for local storage artifacts.
- Keep credential rotation evidence as reviewed summaries, not raw logs or local paths.
- Review at phase gates; keep linked ledgers current.
