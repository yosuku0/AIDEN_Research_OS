# PR-0022: Ledger Structure Validation CI Job

## task_name

Ledger Structure Validation CI Job

## task_description

Add a CI job that validates ledger files have correct structure: approval-record.md has approval_criteria_met field, decision-log.md has required columns, incident-record.md tracks all audit findings.

## boundary_scope

CI workflow enhancement. No schema semantic changes, no runtime code.

## allowed_files

- .github/workflows/governance-ci.yml (add ledger-structure-validation job)

## forbidden_files

- Any ledger file content (read-only validation targets)
- Any schema file (read-only)
- Any script file (read-only)

## human_approval

TRUE

## required_outputs

- .github/workflows/governance-ci.yml with ledger-structure-validation job
- Job checks: approval_criteria_met field presence, decision-log required columns, incident-record audit finding count

## validation_steps

- Validate YAML syntax: `python -c "import yaml; yaml.safe_load(open('.github/workflows/governance-ci.yml'))"` (if pyyaml unavailable, use visual inspection)
- Confirm new job does not break existing artifact-existence, schema-validation, secret-scan, approval-status-check jobs
- Job performs read-only checks (no file modifications)

## incident_trigger

If job requires modifying ledger files (not just reading), STOP and create incident-record.md entry.

## rollback_plan

1. Revert .github/workflows/governance-ci.yml to pre-task state
2. Update decision-log.md to mark this task as "reverted" if DL entry exists

## linked_ledger

DL-0018 area (CI hardening continuation)
