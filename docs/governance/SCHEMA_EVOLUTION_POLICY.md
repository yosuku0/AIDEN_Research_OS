# SCHEMA_EVOLUTION_POLICY

## Purpose

Define JSON Schema versioning, extension, and migration rules to prevent `additionalProperties: false` from blocking legitimate schema evolution.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Current State

All schemas use `additionalProperties: false` with JSON Schema Draft-07 (`$schema: http://json-schema.org/draft-07/schema#`). Audit finding H-004 identified this as technical debt. Audit finding H-006 identified `additionalProperties: false` as blocking future extensions.

## Policy

### Schema Version Migration

| Phase | Target | Timeline | Trigger |
|---|---|---|---|
| Phase 0 (current) | Draft-07 | Now | All existing schemas |
| Phase 1 | 2020-12 | After ADR-0018 Phase 1 approval | Pilot on safe-config.schema.json |
| Phase 2 | 2020-12 | After Phase 1 validation | All governance schemas |
| Phase 3 | 2020-12 | After Phase 2 validation | All research-lab and secret-manager schemas |

### Extension Field Convention

When migrating to 2020-12, use `unevaluatedProperties: false` combined with `patternProperties` to allow experimental extension fields:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "id": { "type": "string" }
  },
  "patternProperties": {
    "^x-[a-z0-9_-]+$": {
      "description": "Experimental extension field. Must start with x-."
    }
  },
  "unevaluatedProperties": false
}
```

Rules for extension fields:
- MUST start with `x-` prefix
- MUST use lowercase, digits, underscore, hyphen only
- SHOULD include a description in the schema
- MAY be promoted to standard fields in a future ADR
- MUST NOT contain credential values, local paths, or execution authority

### Breaking Change Protocol

Any schema change that would cause existing valid fixtures to fail validation is a "breaking change" and requires:
1. ADR update documenting the rationale
2. All fixture updates to remain valid
3. Ledger update recording the change
4. Human approval before merge

## Migration Checklist (Per Schema)

- [ ] Update `$schema` to `https://json-schema.org/draft/2020-12/schema`
- [ ] Replace `additionalProperties: false` with `unevaluatedProperties: false` + `patternProperties` for x- fields
- [ ] Add `$id` with stable URL
- [ ] Verify all existing fixtures still validate
- [ ] Verify unsafe fixtures still fail (where applicable)
- [ ] Update CI to use 2020-12 compatible validator

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/adr/ADR-0018-executable-test-migration.md
