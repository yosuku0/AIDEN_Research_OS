# ADR-0018: Executable Security Test Migration Plan

## Status

Proposed

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

All security tests in the current phase are "documentation-only by design" (ADR-0009). While this preserves the no-runtime boundary, it creates a "governance theater" risk where documented boundaries are not mechanically enforced. The audit fix H-002 (HIGH) identified that zero executable tests means boundary violations cannot be automatically detected at CI time.

This ADR defines a phased, bounded migration from documentation-only tests to executable schema-validated tests, without introducing runtime code, provider integration, or execution authority.

## Decision

Adopt a phased migration plan that introduces executable JSON Schema validation and fixture-based boundary tests, while maintaining the prohibition on runtime implementation, provider integration, and execution authority.

### Phase 1: Schema-Fixture Validation (Immediate)
- Make all CI schema-validation checks run against ALL fixtures (not just no-secret.valid.json)
- Add forbidden-content.cases.json schema validation (verify it FAILS against safe-config.schema.json)
- Introduce `ajv` or `check-jsonschema` as the executable validator in CI

### Phase 2: Approval Record Structure Validation (Short-term)
- Add executable validation that approval-record.md table rows match approval-record.schema.json structure
- Validate that all AR entries have the required `approval_criteria_met` field (post-audit H-001 fix)
- This remains "metadata validation" - no runtime behavior is validated

### Phase 3: Boundary Rule Encoding (Medium-term)
- Encode hard-ban rules from SAFETY.md into executable check script rules
- Examples: verify no .env files, verify no sk- patterns, verify no 0x{40} patterns
- These are already partially implemented in validate-governance.sh but can be expanded

### Phase 4: Codex Task Boundary Verification (Long-term, separate approval)
- Verify that task.md `allowed_files` / `forbidden_files` patterns are syntactically valid
- Cross-check that no task allows forbidden files simultaneously
- This may require parsing task frontmatter - needs separate Human approval

## Rejected Alternatives

- Full runtime integration tests: rejected because it requires runtime implementation, which is out of scope (SAFETY.md hard ban #10)
- Executable tests before boundary approval: rejected because it weakens boundaries, auditability, or Human final approval
- No migration (stay documentation-only): rejected because it leaves boundary violations undetectable at CI time (audit finding H-002)

## Consequences

The repository will gain executable validation for:
1. All JSON fixtures against their schemas (safe fixtures pass, unsafe fixtures fail)
2. Ledger structure compliance against governance schemas
3. Hard-ban pattern detection (expanded from current grep-based approach)

Runtime implementation and provider integration remain out of scope.

## Risks

- Phase scope creep: each phase could expand into de facto runtime testing. Mitigation: each phase requires separate ADR and Human approval.
- Validator dependency: introducing `check-jsonschema` or `ajv` adds a dependency. Mitigation: these are dev-only, CLI tools with no runtime footprint.
- Fixture maintenance: executable tests require fixtures to stay current. Mitigation: fixtures are small JSON files; drift is caught by CI.

## Follow-ups

- Phase 1 requires: update governance-ci.yml schema-validation job, update fixtures to ensure unsafe cases properly fail schema validation
- Phase 2 requires: ADR-0019 (ledger structure validation) with separate Human approval
- Phase 3 requires: expand validate-governance.sh with encoded hard-ban rules
- Phase 4 requires: task parser design ADR with separate Human approval
- Review this ADR at phase gates, keep linked ledgers current.

## Linked Audit Findings

- H-002: HIGH - Documentation-only tests (governance theater)
- This ADR directly addresses H-002 through phased executable test introduction

## Linked Codex Tasks

- PR-0020: Executable test migration (Phase 1 implementation)
