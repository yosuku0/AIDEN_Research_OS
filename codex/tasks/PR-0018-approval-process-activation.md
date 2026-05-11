# PR-0018: Approval Process Activation

## task_name

Approval Process Activation

## task_description

Resolve audit finding H-001 (CRITICAL) by implementing an approval checklist and state transition rules in APPROVAL_FLOW.md, and extending approval-record.md with the approval_criteria_met field.

## boundary_scope

This is a governance control-plane task. It does not grant execution authority, signing authority, or secret custody.

## allowed_files

- docs/governance/APPROVAL_FLOW.md
- research/ledgers/approval-record.md
- docs/governance/LEDGER_SCHEMA.md (read-only reference)

## forbidden_files

- .env
- .env.*
- any runtime source code
- any provider configuration
- any credential file

## human_approval

TRUE

## required_outputs

- docs/governance/APPROVAL_FLOW.md with 8-item Approval Checklist and State Transition Rules
- research/ledgers/approval-record.md with approval_criteria_met field on all AR entries (AR-0001 through AR-0020)
- 3 new AR entries (AR-0018, AR-0019, AR-0020) for audit fix tasks

## validation_steps

- Run scripts/validate-governance.sh and confirm all checks pass
- Confirm all AR entries have approval_criteria_met field
- Confirm APPROVAL_FLOW.md contains checklist table and transition rules table

## incident_trigger

If this task requires modifying forbidden_files or adding runtime code, STOP and create an incident-record.md entry.

## rollback_plan

1. Revert APPROVAL_FLOW.md to pre-task state
2. Revert approval-record.md to 17 AR entries (remove AR-0018 through AR-0020)
3. Update decision-log.md to mark DL-0018 as "reverted"

## linked_ledger

DL-0018, INC-001
