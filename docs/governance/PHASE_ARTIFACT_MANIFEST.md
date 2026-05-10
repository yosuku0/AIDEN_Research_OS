# PHASE_ARTIFACT_MANIFEST

## Purpose

Maps every requested phase to the generated source-of-truth candidate artifacts. This manifest is a review aid and grants no execution authority.

## Phase Map

| Phase | Task | Scope | Primary Artifacts | Gate |
|---|---|---|---|---|
| 0 | PR-0001-root-scaffold | Repository scaffold | README.md; SAFETY.md; docs/system; docs/governance; ADR-0001 through ADR-0004; ledgers; labs; GitHub templates; Codex templates; packages/.gitkeep | PG-0001 |
| 1 | PR-0002-cloud-local-split | Cloud AI and Local AI role split | CLOUD_LOCAL_SPLIT; ADR-0005; TECH_STACK_MATRIX; decision-log DL-0002; open questions | PG-0002 |
| 2 | PR-0003-governance-ledger | Governance ledger schema | LEDGER_SCHEMA; REDACTION_WORKFLOW; schemas/governance; ADR-0006; ledger seed entries | PG-0003 |
| 3 | PR-0004-runtime-boundary | Runtime integration boundary | EXECUTION_BOUNDARY; ADR-0007; ADR-0008; docs/security boundary set | PG-0004 |
| 4 | PR-0005-security-test-plan | Security test plan | RESEARCH_LAB_SECURITY_TEST_PLAN; schemas/research-lab; governance and research-lab fixtures; security and governance test specs; ADR-0009 | PG-0005 |
| 5 | PR-0006-mcp-boundary | MCP boundary and permission model | MCP_BOUNDARY; MCP_TOOL_PERMISSION_MODEL; ADR-0010 | PG-0006 |
| 6 | PR-0007-langgraph-workflow | LangGraph and HITL workflow | LANGGRAPH_WORKFLOW; HITL_APPROVAL_DESIGN; ADR-0011 | PG-0007 |
| 7 | PR-0008-local-storage-sop | Local storage SOP | LOCAL_STORAGE_SOP; ADR-0012 | PG-0008 |
| 8 | PR-0009-credential-rotation | Credential rotation execution SOP | CREDENTIAL_ROTATION_SOP; ADR-0013 | PG-0009 |
| 9 | PR-0010-secret-manager-selection | Secret manager selection | SECRET_MANAGER_SELECTION | PG-0010 |
| 10 | PR-0011-readiness-review | Secret manager readiness review | SECRET_MANAGER_READINESS; ADR-0014 | PG-0011 |
| 11 | PR-0012-narrow-implementation-plan | Narrow implementation plan | SECRET_MANAGER_NARROW_PLAN; SECRET_CUSTODY_BOUNDARY; LOCAL_ARTIFACT_STORAGE_BOUNDARY; SECRET_MANAGER_SECURITY_TEST; ADR-0015 | PG-0012 |
| 12 | PR-0013-minimal-impl-task-design | Minimal implementation task design | MINIMAL_IMPL_TASK_DESIGN | PG-0013 |
| 13 | PR-0014-minimal-impl-final-gate | Minimal implementation final gate | MINIMAL_IMPL_FINAL_GATE | PG-0014 |
| 14 | PR-0015-minimal-implementation | Secret manager minimal implementation | MINIMAL_IMPL_SCOPE; schemas/secret-manager/safe-config.schema.json; fixtures/security/secret-manager; secret-manager-content-path-check; ADR-0017 | PG-0015 |
| 15 | PR-0016-os-keychain-boundary | OS keychain adapter boundary | OS_KEYCHAIN_BOUNDARY; ADR-0016 | PG-0016 |
| 16 | PR-0017-os-keychain-adapter | OS keychain adapter task design | OS_KEYCHAIN_ADAPTER_TASK | PG-0017 |

## Review Notes

All rows remain Hold until Human review. The manifest does not replace ADRs, ledgers, pull request review, CODEOWNERS, or approval-record.md.

## References

SAFETY.md; docs/system/PRODUCT_BOUNDARY.md; docs/system/EXECUTION_BOUNDARY.md; research/ledgers/phase-gate-record.md.
