# ADR-0013: Credential Rotation Execution

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Define human-approved rotation procedures without implementing runtime rotation.

## Rejected Alternatives

- AI-initiated rotation: rejected because it weakens boundaries, auditability, or Human final approval.
- Provider-specific automation now: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Human rotation procedure may be skipped under incident pressure if responsibilities are not explicit.
- Rotation timing may leave stale references in governance artifacts if follow-up review is missed.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Keep rotation steps manual and Human-owned until a separate approval authorizes any automation.
- Review approval records after each rotation event to ensure references remain metadata-only.
- Review at phase gates; keep linked ledgers current.
