---
task_id: PR-0006
title: MCP Boundary and Tool Permission Model
task_class: governance-docs-only
risk_level: high
status: ready
human_approval_required: true
---

# Goal
MCP アーキテクチャの境界とツール権限モデルを定義する。

# Inputs
- RS-06 MCP Boundary and Tool Permission Model
- RS-06B Artifact Sheet

# In Scope
- docs/governance/MCP_BOUNDARY.md
- docs/governance/MCP_TOOL_PERMISSION_MODEL.md
- docs/adr/ADR-0010-mcp-boundary-tool-permission.md
- research/ledgers/ 更新

# Allowed Files
- docs/governance/MCP_BOUNDARY.md
- docs/governance/MCP_TOOL_PERMISSION_MODEL.md
- docs/adr/ADR-0010*.md
- research/ledgers/*.md

# Acceptance Criteria
- Host-client-server 分離が明確
- ツール権限マトリクスが定義されている
- Roots are advisory only と記載されている
