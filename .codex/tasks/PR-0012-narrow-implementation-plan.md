---
task_id: PR-0012
title: Secret Manager Narrow Implementation Plan
task_class: governance-docs-only
risk_level: high
status: ready
human_approval_required: true
---

# Goal
Secret Manager と local-only artifact storage の narrow implementation plan を governance artifact として確定する。実装ではなく計画のみ。

# Inputs
- RS-12 Secret Manager Narrow Implementation Plan
- RS-11B Readiness Gate constraints

# In Scope
- docs/governance/SECRET_MANAGER_NARROW_PLAN.md
- docs/governance/SECRET_CUSTODY_BOUNDARY.md
- docs/governance/LOCAL_ARTIFACT_STORAGE_BOUNDARY.md
- docs/governance/SECRET_MANAGER_SECURITY_TEST.md
- docs/adr/ADR-0015-secret-manager-narrow-impl.md
- research/ledgers/risk-ledger.md 追記
- research/ledgers/decision-log.md 追記
- research/ledgers/open-questions.md 追記

# Out of Scope
- Secret manager 実装
- Local storage 実装
- Encryption 実装
- Purge automation 実装
- Credential rotation 実装
- Provider-specific operation
- CI / GitHub Actions
- Runtime code

# Allowed Files
- docs/governance/SECRET_MANAGER_NARROW_PLAN.md
- docs/governance/SECRET_CUSTODY_BOUNDARY.md
- docs/governance/LOCAL_ARTIFACT_STORAGE_BOUNDARY.md
- docs/governance/SECRET_MANAGER_SECURITY_TEST.md
- docs/adr/ADR-0015*.md
- research/ledgers/*.md

# Required Outputs
1. SECRET_MANAGER_NARROW_PLAN.md: narrow scope, candidate target matrix, minimal viable secret custody scope, minimal local artifact storage scope, owner/reviewer/approver model, implementation preconditions, Go/No-Go/Hold rules
2. SECRET_CUSTODY_BOUNDARY.md: allowed custody targets, forbidden custody (private keys, production credentials, wallet/signer)
3. LOCAL_ARTIFACT_STORAGE_BOUNDARY.md: storage targets, retention posture per artifact class, purge requirements, GitHub promotion rules (redacted only)
4. SECRET_MANAGER_SECURITY_TEST.md: security test handoff requirements, design rules under test
5. ADR-0015: Status=Accepted, explicit non-goals (NO implementation), allowed: docs-only planning, schema-only safe config

# Acceptance Criteria
- すべての governance doc に必要な見出しが存在する
- ADR-0015 に rejected alternatives と consequences が含まれる
- 禁止保管対象が明示されている
- narrow implementation approval が execution approval ではないと明記
