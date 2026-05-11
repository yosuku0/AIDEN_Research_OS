---
task_id: PR-0016
title: OS Keychain Adapter Boundary
task_class: governance-docs-only
risk_level: high
status: ready
human_approval_required: true
---

# Goal
OS Keychain Adapter の境界を固定する。実装ではなく境界定義のみ。

# Inputs
- RS-16 OS Keychain Adapter Boundary
- RS-16B Artifact Sheet

# In Scope
- docs/governance/OS_KEYCHAIN_BOUNDARY.md
- docs/adr/ADR-0016-os-keychain-adapter.md
- research/ledgers/ 更新

# Out of Scope
- OS keychain adapter の実装コード
- Secret custody 実装
- ランタイム統合

# Allowed Files
- docs/governance/OS_KEYCHAIN_BOUNDARY.md
- docs/adr/ADR-0016*.md
- research/ledgers/*.md

# Required Outputs
1. OS_KEYCHAIN_BOUNDARY.md:
   - Adapter scope and limitations
   - Allowed operations (read metadata only, no credential values)
   - Forbidden operations (secret retrieval, secret storage, key generation)
   - Error handling requirements
   - Incident triggers for boundary breach

2. ADR-0016:
   - Status: Draft for PR-0017
   - Context: PR-0015 completed, next natural step
   - Decision: Fix boundary before implementation
   - Allowed: API surface design, forbidden data classification, rollback plan
   - Forbidden: implementation code, secret access, runtime custody

# Acceptance Criteria
- 境界が明確に定義されている
- Forbidden operations が明示されている
- Incident triggers が定義されている
