# AUTONOMY_TIER_POLICY

## Purpose

Define machine-enforced eligibility for Codex-driven development while preserving Human gates for restricted areas.

## Tiers

- Tier 0 (safe auto): docs, non-sensitive fixtures, and tests.
- Tier 1 (guarded auto): package/runtime changes with full CI pass.
- Tier 2 (human required): approval policy, safety boundary, and ownership control files.

## Tier 2 Restricted Files

- `.github/CODEOWNERS`
- `SAFETY.md`
- `docs/system/PRODUCT_BOUNDARY.md`
- `AGENTS.md`
- `research/ledgers/approval-record.md`
- `research/ledgers/phase-gate-record.md`

## CI Enforcement Requirements

1. Governance validation must pass.
2. Lint/type/unit tests must pass for package changes.
3. If a PR touches Tier 2 restricted files, the pipeline reports `HUMAN_REVIEW_REQUIRED`.

## Operational Rule

No automation path may auto-approve a phase explicitly marked as human approval required.
