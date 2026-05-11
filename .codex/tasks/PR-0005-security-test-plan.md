---
task_id: PR-0005
title: Research Lab Security Test Plan
task_class: governance-docs-only
risk_level: high
status: ready
human_approval_required: true
---

# Goal
リサーチラボの包括的セキュリティテスト計画を作成する。

# Inputs
- RS-05 Research Lab Security Test Plan
- RS-05B Artifact Sheet

# In Scope
- docs/governance/RESEARCH_LAB_SECURITY_TEST_PLAN.md
- schemas/research-lab/*.json
- fixtures/governance/*.json, fixtures/research-lab/safe/*, fixtures/research-lab/unsafe/*
- docs/adr/ADR-0009-research-lab-security-test-plan.md
- tests/security/*.md, tests/governance/*.md
- research/ledgers/ 更新

# Allowed Files
- docs/governance/RESEARCH_LAB_SECURITY_TEST_PLAN.md
- docs/adr/ADR-0009*.md
- schemas/research-lab/*.json
- fixtures/**/*.json
- tests/**/*.md
- research/ledgers/*.md

# Acceptance Criteria
- テスト計画が包括的
- Safe/unsafe 両方のフィクスチャが定義されている
- すべてのテストは Markdown 仕様のみ（実行可能スクリプトなし）
