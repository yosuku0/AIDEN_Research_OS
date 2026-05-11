# incident-record

## Schema Reference

docs/governance/LEDGER_SCHEMA.md

## Open Incidents

| id | scope | finding_id | description | severity | detected_at | reported_by | status | resolution_plan | resolved_at | resolution_summary | approver |
|---|---|---|---|---|---|---|---|---|---|---|---|
| INC-001 | APPROVAL_PROCESS | H-001 | All 17 ARs remain "hold" with no defined state transition criteria. Approval process is stalled. Human approvers lack checklist for transitioning to "approve". | CRITICAL | 2026-05-11 | Audit (Orchestrator) | open | Implement APPROVAL_FLOW.md checklist (8 items) and state transition rules; add approval_criteria_met field to all AR entries. | pending | APPROVAL_FLOW.md updated; AR-0018 through AR-0020 created; awaiting Human review. | Human |
| INC-002 | SECURITY_TESTING | H-002 | All security tests are "documentation-only by design". Zero executable tests means boundary violations cannot be automatically detected at CI time. | HIGH | 2026-05-11 | Audit (Orchestrator) | open | Create ADR-0018 (Executable Test Migration Plan); implement Phase 1: executable schema-fixture validation in CI. | pending | ADR-0018 created; CI schema-validation job expanded; awaiting Human approval for "Proposed" status. | Human |
| INC-003 | CI_SECURITY | H-003 | Secret scan in validate-governance.sh wrote matched content to a temporary scan file and displayed it in CI logs, risking information leakage. | HIGH | 2026-05-11 | Audit (Orchestrator) | open | Replace temp file handling with pipe processing; output file paths only and never matched content. | pending | validate-governance.sh and governance-ci.yml updated; awaiting Human review. | Human |
| INC-004 | SCHEMA_VERSION | H-004 | All 11 JSON Schemas use Draft-07 (2017). Modern features (if/then/else, unevaluatedProperties) unavailable. | MEDIUM | 2026-05-11 | Audit (Orchestrator) | open | Create SCHEMA_EVOLUTION_POLICY.md; pilot migration of safe-config.schema.json to 2020-12. | pending | SCHEMA_EVOLUTION_POLICY.md created; pilot migration deferred to post-ADR-0018 Phase 1. | Human |
| INC-005 | ADR_QUALITY | H-005 | All 17 ADRs have identical Risks and Follow-ups sections (mechanical copy-paste), diluting ADR-specific risk analysis. | MEDIUM | 2026-05-11 | Audit (Orchestrator) | open | Create ADR_DIFFERENTIATION_GUIDE.md; backfill differentiated Risks/Follow-ups for priority ADRs. | pending | ADR_DIFFERENTIATION_GUIDE.md created; ADR-0005 and ADR-0011 differentiated as examples. | Human |
| INC-006 | SCHEMA_EXTENSIBILITY | H-006 | All schemas use additionalProperties: false, blocking future field additions without breaking changes. | MEDIUM | 2026-05-11 | Audit (Orchestrator) | open | Use unevaluatedProperties: false with x- prefix patternProperties after 2020-12 migration. | pending | Documented in SCHEMA_EVOLUTION_POLICY.md; deferred to 2020-12 migration. | Human |
| INC-007 | REPOSITORY_CONFIG | H-007 | CODEOWNERS uses placeholder @repo-owner instead of actual GitHub username/team. | LOW | 2026-05-11 | Audit (Orchestrator) | open | Add replacement instructions to CODEOWNERS; require Human to replace with actual value. | pending | CODEOWNERS updated with instructions and audit reference. | Human |

## Resolved Incidents

| id | scope | finding_id | description | severity | detected_at | reported_by | status | resolution_plan | resolved_at | resolution_summary | approver |
|---|---|---|---|---|---|---|---|---|---|---|---|
| INC-008 | PACKAGE_IMPORT | H-003 | Untracked source package artifact included a fixture with a secret-like pattern. Repository fixture was sanitized, and distribution package files are ignored from commit scope. | HIGH | 2026-05-11 | Codex | resolved | Keep codex-app-package/ untracked and ignored; never stage distribution package artifacts. | 2026-05-11 | R1 verification confirmed codex-app-package/ is not tracked and .gitignore contains codex-app-package/. | Human |

## Incident Response Procedure

1. When an incident is detected, create an entry in this table
2. Link to the related decision-log entry
3. Create a Codex task for remediation (if applicable)
4. Human approver reviews and decides: resolve / escalate / accept risk
5. On resolution: fill resolved_at, resolution_summary, and approver fields
6. Update linked phase-gate-record.md if phase gate decision changes

## References

docs/governance/APPROVAL_FLOW.md, docs/governance/LEDGER_SCHEMA.md, research/ledgers/decision-log.md
