---
task_id: PR-0004
title: AIDEN Runtime Integration Boundary
task_class: governance-docs-only
risk_level: high
status: ready
human_approval_required: true
---

# Goal
AIDEN Runtime の境界定義とセキュリティテストハンドオフを文書化する。

# Inputs
- RS-04 AIDEN Runtime Integration Boundary
- RS-04B, RS-04C

# In Scope
- docs/system/EXECUTION_BOUNDARY.md
- docs/adr/ADR-0007-runtime-integration-boundary.md
- docs/adr/ADR-0008-aiden-runtime-boundary.md
- docs/security/ 以下の全セキュリティ文書
- research/ledgers/ 更新

# Allowed Files
- docs/system/EXECUTION_BOUNDARY.md
- docs/adr/ADR-0007*.md, ADR-0008*.md
- docs/security/*.md
- research/ledgers/*.md

# Required Outputs
1. EXECUTION_BOUNDARY.md: runtime boundary, artifact boundary, human gate, release gate, forbidden actions
2. ADR-0007, ADR-0008
3. HARDENING_POSTURE.md, THREAT_MODEL.md, HUMAN_APPROVAL_KILL_SWITCH.md, PRODUCTION_EXECUTION_PROHIBITION.md, MODEL_ROUTING_COST_LIMITS.md, NETWORK_RPC_ALLOWLIST.md, SIMULATION_EVIDENCE_FORMAT.md, AUDIT_LEDGER.md

# Acceptance Criteria
- 境界が明確に定義されている
- 禁止事項が明示されている
- Human approval gate がすべての重要決定に必要であることが記載されている
