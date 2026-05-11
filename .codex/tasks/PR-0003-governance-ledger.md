---
task_id: PR-0003
title: Governance Ledger Schema and Redaction Workflow
task_class: governance-docs-only
risk_level: medium
status: ready
human_approval_required: true
---

# Goal
Governance Ledger の完全なスキーマ体系と Redaction Workflow を確立する。

# Inputs
- RS-03 Governance Ledger Schema and Redaction Workflow
- RS-03A Final Governance Ledger Artifact Sheet

# In Scope
- docs/governance/LEDGER_SCHEMA.md の作成（8つの台帳スキーマ）
- docs/governance/REDACTION_WORKFLOW.md の作成
- schemas/governance/*.json の作成（4つのJSONスキーマ）
- docs/adr/ADR-0006-governance-ledger-schema.md の作成
- research/ledgers/ の初期エントリ更新

# Out of Scope
- 台帳の自動化スクリプト
- CI 統合
- 暗号化実装
- ランタイムコード

# Allowed Files
- docs/governance/LEDGER_SCHEMA.md
- docs/governance/REDACTION_WORKFLOW.md
- docs/adr/ADR-0006-governance-ledger-schema.md
- schemas/governance/*.json
- research/ledgers/*.md

# Required Outputs
1. LEDGER_SCHEMA.md with schemas for: decision-log, risk-ledger, approval-record, redaction-checklist, incident-record, task-promotion-record, open-questions, phase-gate-record
2. REDACTION_WORKFLOW.md: redaction required before GitHub promotion, raw data never promoted in raw form, failure → stop + isolate + incident-record
3. JSON schemas for all ledger types
4. ADR-0006
5. Ledger initial entries

# Acceptance Criteria
- すべての台帳スキーマが定義されている
- Redaction workflow が明確
- approval-record.md が canonical approval として位置づけられている
