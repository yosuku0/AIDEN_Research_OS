---
task_id: PR-0015
title: Secret Manager Minimal Implementation
task_class: minimal-safe-implementation
risk_level: high
status: ready-for-human-approval
human_approval_required: true
---

# Goal
Secret Manager readiness の最小安全実装面を作成する。

# Background
PR-0014 で final gate を通過した後、最初の narrow implementation surface。
GitHub は approved artifact only の Source of Truth。
GitHub must not store credential values, local secret paths, raw prompts, raw model outputs, raw local runtime logs。
approval-record.md is canonical Human approval。
PR-0015 approval is not execution approval。

# Inputs
- RS-15 Secret Manager Minimal Implementation
- RS-14 Secret Manager Minimal Implementation Final Gate

# In Scope
- safe config schema (schemas/secret-manager/safe-config.schema.json)
- no-secret valid fixture (fixtures/security/secret-manager/no-secret.valid.json)
- forbidden-content fixtures (fixtures/security/secret-manager/forbidden-content.cases.json)
- content/path security check 仕様 (tests/security/secret-manager-content-path-check.md)
- ADR-0018 草案 (docs/adr/ADR-0018-secret-manager-minimal-implementation.md)
- governance doc (docs/governance/SECRET_MANAGER_MINIMAL_IMPLEMENTATION.md)
- ledger draft entries
- PR-0015 task file

# Out of Scope
- secret manager runtime
- OS keychain adapter
- local encrypted vault
- credential rotation
- provider-specific operations
- CI / GitHub Actions
- runtime code
- package install

# Allowed Files
- docs/adr/ADR-0018-secret-manager-minimal-implementation.md
- docs/governance/SECRET_MANAGER_MINIMAL_IMPLEMENTATION.md
- schemas/secret-manager/safe-config.schema.json
- fixtures/security/secret-manager/no-secret.valid.json
- fixtures/security/secret-manager/forbidden-content.cases.json
- tests/security/secret-manager-content-path-check.md
- research/ledgers/*.md
- codex/tasks/PR-0015-secret-manager-minimal-implementation/task.md

# Forbidden Files
- .env, .env.*
- runtime/**
- src/**
- .github/workflows/**
- package.json
- any wallet/signer/deploy/execution file

# Required Outputs
1. ADR-0018: Status, Context, Decision, Minimal Implementation Scope, Safe Schema Boundary, Fixture Boundary, Content/Path Check Boundary, Human Approval Gate, Rollback Plan, Incident Triggers, Consequences, Rejected Alternatives, Follow-ups
2. SECRET_MANAGER_MINIMAL_IMPLEMENTATION.md: Purpose, Scope, Safe Schema Requirements, Fixture Requirements, Content/Path Check Requirements, Human Approval Gate, Rollback Plan, Incident Triggers, Non-Goals
3. safe-config.schema.json: secret reference metadata only, no credential value field, no local path field, no provider operation field, no execution approval field
4. no-secret.valid.json: valid no-secret fixture, no credential values, no local paths
5. forbidden-content.cases.json: safe abstract negative cases, no real-looking secrets
6. secret-manager-content-path-check.md: content/path check specification, no executable scripts, no package install
7. Ledger draft entries
8. Self-contained task.md

# Prohibited Work
- Do not implement secret manager runtime
- Do not implement OS keychain adapter
- Do not implement local encrypted vault
- Do not include credential values or examples
- Do not include local path values
- Do not modify CI / GitHub Actions
- Do not add package installs or dependencies
- Do not treat approval as execution approval
- Do not edit files outside allowed_files

# Acceptance Criteria
- All required outputs exist
- ADR-0018 has all required headings
- Schema excludes forbidden fields
- Fixtures contain no secret-like values
- Content/path check spec has no executable code
- No prohibited work present
