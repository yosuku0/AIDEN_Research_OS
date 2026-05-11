---
task_id: PR-0008
title: Local Storage and Credential Rotation SOP
task_class: governance-docs-only
risk_level: high
status: ready
human_approval_required: true
---

# Goal
ローカル専用ストレージポリシーとクレデンシャルローテーション手順を定義する。

# Inputs
- RS-08 Local Storage and Credential Rotation SOP
- RS-08B Artifact Sheet

# In Scope
- docs/governance/LOCAL_STORAGE_SOP.md
- docs/adr/ADR-0012-local-storage-credential-rotation.md
- research/ledgers/ 更新

# Allowed Files
- docs/governance/LOCAL_STORAGE_SOP.md
- docs/adr/ADR-0012*.md
- research/ledgers/*.md

# Acceptance Criteria
- ローカルワークスペースの定義が明確
- 保持期間ポリシーが定義されている
- GitHub 昇格は redacted summary のみと記載
- Purge 要件が明確
