# ADR-0019: Autonomy Transition Tiering for Codex-Driven Development

## Status

Proposed

## Context

The project currently enforces Human approval gates for phase progression and prohibits auto-approval of Human gate items. This protects governance integrity, but it blocks a full move to Codex-led development throughput.

## Decision

Adopt a tiered autonomy transition model:

- **Tier 0 (safe auto)**: docs, fixtures, and non-sensitive tests can be merged with automated checks only.
- **Tier 1 (guarded auto)**: package/runtime code can be merged when governance + lint + type + unit checks pass and no restricted files are changed.
- **Tier 2 (human required)**: security boundaries, authority/approval policies, and restricted governance files always require explicit Human approval.

The transition runs in three implementation phases:
1. Governance redesign PRs (policy + ledgers + ADR alignment).
2. CI policy enforcement (machine-enforced autonomy eligibility checks).
3. Ordered execution of implementation ladder with automation defaults and Human escalation only for Tier 2.

## Rejected Alternatives

- Immediate full auto-merge for all files: rejected due to boundary and audit risk.
- Permanent Human-only approvals for every PR: rejected due to throughput constraints.

## Consequences

Automation can increase safely for low-risk changes while preserving hard governance boundaries and auditability.

## Risks

- Misclassification of risky changes as low-risk could bypass intended review.
- CI policy drift could create gaps between documented and enforced rules.

## Follow-ups

- Add CI check that classifies changed files and fails when Tier 2 files are touched without explicit override marker.
- Track weekly metrics: auto-merge ratio, CI failure rate, human rollback rate.
- Revisit tier definitions after four weeks of telemetry.
