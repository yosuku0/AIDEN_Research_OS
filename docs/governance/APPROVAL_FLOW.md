# APPROVAL_FLOW

## Purpose

Defines Human approval process with approval-record.md as canonical.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Policy

Reviewed artifacts are promoted only after redaction, ledger linkage, and review. Human approval remains final for restricted decisions.

## Procedure

Create the artifact, link ADRs and ledgers, complete redaction checks, request review, and record approval or hold status.

## Approval Checklist

Before changing an AR (Approval Record) from "hold" to "approve", the approver MUST verify ALL of the following:

| # | Check Item | Verification Method | Evidence Location |
|---|---|---|---|
| 1 | All required outputs in the linked Codex task exist | Cross-check task.required_outputs against actual files | File system / Git diff |
| 2 | No forbidden files were modified | Cross-check modified files against task.forbidden_files | `git diff --name-only` |
| 3 | Secret scan passes with zero failures | Run `scripts/validate-governance.sh` or CI secret-scan job | CI logs / local terminal |
| 4 | Schema validation passes (if schemas modified) | Run `check-jsonschema --check-metaschema` on modified schemas | CI schema-validation job |
| 5 | Redaction checklist is complete | Verify research/ledgers/redaction-checklist.md has all true values | Ledger file |
| 6 | Cross-references to ADRs and ledgers are present | Verify all linked_adr and linked_ledger entries resolve | Manual review |
| 7 | Human approver identity and timestamp recorded | Approval record includes approver name and ISO-8601 timestamp | approval-record.md |
| 8 | No execution authority granted in artifacts | Verify no signer, deploy, swap, bridge, transfer language | Manual review + grep |

## State Transition Rules

| From | To | Condition | Action |
|---|---|---|---|
| hold | approve | All 8 checklist items pass + Human approver identity recorded | Update approval-record.md; set timestamp; close linked phase gate |
| hold | edit | Any checklist item fails (non-critical) | Return to responsible node with specific edit requests in comments |
| hold | reject | Boundary drift, secret exposure, or execution authority detected | Stop; create incident-record entry; mark phase gate "no-go" |
| approve | hold | Only via incident escalation with new Human review | Reopen phase gate; require new approval cycle |
| pending | hold | Initial state after artifact creation | Default; requires explicit Human review to transition |

## Approval Record Schema Extension

Each approval record entry MUST include the following fields:

| Field | Required | Description |
|---|---|---|
| id | yes | AR-XXXX format |
| approval_type | yes | Type of approval requested |
| requested_by | yes | Entity requesting approval |
| approver | yes | Human approver identity (not "Human" placeholder) |
| approval_scope | yes | Scope of the approval |
| linked_pr | no | Linked pull request |
| linked_phase_gate | yes | Linked phase gate ID |
| decision | yes | One of: pending, hold, approve, edit, reject |
| conditions | no | Conditions or caveats |
| approval_criteria_met | yes | Checklist completion status (JSON array of booleans) |
| timestamp | yes | ISO-8601 timestamp or "pending" |

## Rollback

If approval is revoked or incident is detected:
1. Mark the AR as "hold" with incident reference
2. Update linked phase-gate-record.md with "hold" decision
3. Create or update incident-record.md entry
4. Notify all CODEOWNERS

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, research/ledgers/approval-record.md, research/ledgers/phase-gate-record.md.

## Autonomy Execution Gate (Tiered)

To support Codex-led execution for remaining implementation phases, CI computes autonomy eligibility using `scripts/check-autonomy-eligibility.sh`.

- `AUTO_EXECUTE_OK=true` when no Tier 2 restricted files changed and baseline governance checks pass.
- `HUMAN_REVIEW_REQUIRED=true` when restricted governance boundary files are changed.
- Any phase explicitly marked as human-required remains hold/pending until Human decision is recorded in `research/ledgers/approval-record.md`.
