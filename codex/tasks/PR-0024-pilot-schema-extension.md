# PR-0024: Pilot Schema Extension (2020-12)

## task_name

Pilot Schema Extension with x- Prefix Support

## task_description

Apply unevaluatedProperties: false + patternProperties for x- prefixed extension fields to safe-config.schema.json (already migrated to 2020-12). This enables future experimental field additions without breaking changes.

## boundary_scope

Schema structure enhancement. No semantic changes, no runtime code.

## allowed_files

- schemas/secret-manager/safe-config.schema.json (add patternProperties only)

## forbidden_files

- Any fixture file (read-only validation target)
- Any other schema file
- Any ledger file

## human_approval

TRUE

## required_outputs

- safe-config.schema.json has patternProperties with ^x-[a-z0-9_-]+$ regex
- safe-config.schema.json uses unevaluatedProperties: false (replacing additionalProperties: false)
- Description in patternProperties explains x- field conventions

## validation_steps

- check-jsonschema --check-metaschema schemas/secret-manager/safe-config.schema.json passes
- no-secret.valid.json validates against updated schema
- forbidden-content.cases.json fails against updated schema (expected)
- A new test with x- prefixed field validates (create temporary test locally, do not commit)

## incident_trigger

If schema semantic meaning changes (required fields added/removed, property types changed), STOP and create incident-record.md entry. Only structural changes (patternProperties, unevaluatedProperties) are allowed.

## rollback_plan

1. Revert safe-config.schema.json to pre-task state
2. Update decision-log.md if DL entry was added

## linked_ledger

INC-004 (H-004 resolution), INC-006 (H-006 resolution)
