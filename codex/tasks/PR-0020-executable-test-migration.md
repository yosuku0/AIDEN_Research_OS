# PR-0020: Executable Test Migration

## task_name

Executable Test Migration Phase 1

## task_description

Resolve audit finding H-002 (HIGH) by introducing executable schema-fixture validation. Create ADR-0018 documenting the phased migration plan, and expand CI schema-validation job to validate ALL fixtures against their schemas.

## boundary_scope

This is a governance control-plane task. It introduces executable validation of documentation artifacts, not runtime tests.

## allowed_files

- docs/adr/ADR-0018-executable-test-migration.md
- .github/workflows/governance-ci.yml (schema-validation job)
- fixtures/security/secret-manager/forbidden-content.cases.json (read-only validation target)
- fixtures/security/secret-manager/no-secret.valid.json (read-only validation target)

## forbidden_files

- .env
- .env.*
- any runtime source code
- any provider configuration
- any credential file
- schemas/secret-manager/safe-config.schema.json (read-only reference)

## human_approval

TRUE

## required_outputs

- docs/adr/ADR-0018-executable-test-migration.md with 4-phase plan
- .github/workflows/governance-ci.yml: schema-validation job validates all fixtures
- CI validates no-secret.valid.json PASSES safe-config.schema.json
- CI validates forbidden-content.cases.json FAILS safe-config.schema.json (expected)

## validation_steps

- Confirm ADR-0018 has Status "Proposed" with all required sections
- Confirm CI schema-validation job includes fixture validation step
- Confirm decision-log.md has DL-0020 entry
- Run CI workflow on test branch and confirm expected pass/fail results

## incident_trigger

If task scope expands to runtime testing or requires modifying schema semantic meaning, STOP and create incident-record.md entry.

## rollback_plan

1. Remove ADR-0018 file
2. Revert .github/workflows/governance-ci.yml schema-validation job
3. Update decision-log.md to mark DL-0020 as "reverted"
4. Update incident-record.md INC-002 to "reopened"

## linked_ledger

DL-0020, INC-002
