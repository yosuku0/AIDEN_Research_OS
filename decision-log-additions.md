# decision-log (append these entries to research/ledgers/decision-log.md)

## New Entries — PR-0018 through PR-0019

Append the rows below to the existing Entries table in decision-log.md.

| id | decision_type | status | owner | linked_adr | linked_codex_task | decision | alternatives | rationale | consequences | rollback_plan |
|---|---|---|---|---|---|---|---|---|---|---|
| DL-0018 | ci enforcement | proposed | Human | ADR-0018 | PR-0018-ci-hardening | Replace file-existence CI with 6-job governance pipeline including schema validation, secret scan, ADR structure check, and Python test execution. | Keep existing CI and add comments; adopt third-party secret scanner only | Audit CRIT-01 requires executable enforcement — documentation-only governance is insufficient for security-critical paths. | All PRs now run 6 CI jobs. Secret-like patterns and invalid JSON block merge. Local validate-governance.sh enables pre-commit checks. | Revert governance-ci.yml; restore original 1-job file-existence check; open incident-record for CRIT-01 regression. |
| DL-0019 | implementation start | proposed | Human | ADR-0018 | PR-0019-core-implementation | Create packages/aiden-core Python package with Pydantic settings, KeychainAdapter, LangGraph stub, LiteLLM router stub, FastMCP stub, Langfuse tracer stub, and pytest conftest. | Continue docs-only indefinitely | Phase gate record PG-0019 requires human approval. Implementation cannot proceed without a package structure. | packages/ directory is now non-empty. pip install -e ".[dev]" must succeed. All stubs pass pytest. | Delete packages/aiden-core/; restore packages/.gitkeep. |
