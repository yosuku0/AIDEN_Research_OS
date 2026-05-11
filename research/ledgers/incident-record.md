# incident-record

## Schema Reference

docs/governance/LEDGER_SCHEMA.md

## Open Incidents

None. All audit findings resolved.

## Resolved Incidents

| id | scope | finding_id | description | severity | detected_at | reported_by | status | resolution_plan | resolved_at | resolution_summary | approver |
|---|---|---|---|---|---|---|---|---|---|---|---|
| INC-001 | APPROVAL_PROCESS | H-001 | All 17 ARs remain "hold" with no defined state transition criteria. | CRITICAL | 2026-05-11 | Audit | resolved | Implement APPROVAL_FLOW.md checklist and state transition rules. | 2026-05-11 | APPROVAL_FLOW.md updated with 8-item checklist and state transition table; approval-record.md extended with approval_criteria_met field. | Human |
| INC-002 | SECURITY_TESTING | H-002 | All security tests are documentation-only. Zero executable runtime validation. | HIGH | 2026-05-11 | Audit | resolved | Create ADR-0018; implement Phase 1 executable schema-fixture validation. | 2026-05-11 | ADR-0018 created; CI schema-validation job expanded to validate all fixtures against schemas; 22 fixture pairs created. | Human |
| INC-003 | CI_SECURITY | H-003 | Secret scan writes matched content to /tmp and CI logs. | HIGH | 2026-05-11 | Audit | resolved | Replace temp file with pipe; output file paths only. | 2026-05-11 | validate-governance.sh and governance-ci.yml updated; no temp file usage; file-path-only output; cleanup command added. | Human |
| INC-004 | SCHEMA_VERSION | H-004 | All schemas use Draft-07 (2017). Modern features unavailable. | MEDIUM | 2026-05-11 | Audit | resolved | Create SCHEMA_EVOLUTION_POLICY.md; migrate all schemas to 2020-12. | 2026-05-11 | SCHEMA_EVOLUTION_POLICY.md created; all 12 schemas migrated to 2020-12 with $id; unevaluatedProperties enabled. | Human |
| INC-005 | ADR_QUALITY | H-005 | All 17 ADRs have identical Risks/Follow-ups (mechanical copy-paste). | MEDIUM | 2026-05-11 | Audit | resolved | Create ADR_DIFFERENTIATION_GUIDE.md; backfill all ADRs. | 2026-05-11 | ADR_DIFFERENTIATION_GUIDE.md created; all 17 ADRs differentiated with ADR-specific risks and follow-ups. | Human |
| INC-006 | SCHEMA_EXTENSIBILITY | H-006 | additionalProperties: false blocks future field additions. | MEDIUM | 2026-05-11 | Audit | resolved | Use unevaluatedProperties: false with x- prefix patternProperties. | 2026-05-11 | All 12 schemas updated with patternProperties ^x-[a-z0-9_-]+$ and unevaluatedProperties: false. | Human |
| INC-007 | REPOSITORY_CONFIG | H-007 | CODEOWNERS uses placeholder @repo-owner. | LOW | 2026-05-11 | Audit | resolved | Human replaces placeholder with actual GitHub handle per ADR-0019. | 2026-05-11 | CODEOWNERS updated with actual owner handle; ADR-0019 exemption applied. | Human |
| INC-008 | CODEX_STOP | V1_STOP | Codex V1 stopped due to secret-like pattern in forbidden-content fixture and untracked codex-app-package/ directory. | MEDIUM | 2026-05-11 | Codex | resolved | Fix fixture to use abstract markers; add codex-app-package/ to .gitignore. | 2026-05-11 | forbidden-content.cases.json uses structural mismatch (no credential literals); .gitignore excludes codex-app-package/. | Human |

## Incident Response Procedure

1. When an incident is detected, create an entry in this table
2. Link to the related decision-log entry
3. Create a Codex task for remediation (if applicable)
4. Human approver reviews and decides: resolve / escalate / accept risk
5. On resolution: fill resolved_at, resolution_summary, and approver fields
6. Update linked phase-gate-record.md if phase gate decision changes

## References

docs/governance/APPROVAL_FLOW.md, docs/governance/LEDGER_SCHEMA.md, research/ledgers/decision-log.md
