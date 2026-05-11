# MCP Tool Permission Matrix

## Purpose

Concrete tool permission matrix for the Model Context Protocol (MCP) integration, based on ADR-0010 and MCP_BOUNDARY.md.

## Permission Model

Host owns all tool permissions. Only minimum necessary tools are granted per role.

## Tool List

| Tool | Read | Write | Execute | Notes |
|---|---|---|---|---|
| file_read | All roles | None | None | Read allowed_files only |
| file_write | None | Codex | None | Write allowed_files only |
| git_status | All roles | None | None | Read-only repository state |
| shell_exec | None | None | None | **Prohibited** - no shell access |
| http_request | None | None | None | **Prohibited** - no external calls |
| schema_validate | All roles | None | None | Read-only validation |
| ledger_read | Human, Reviewer | None | None | Read-only ledger access |
| ledger_write | None | Human | None | Human approval required |

## Role Mapping

| Role | Tools Granted | Approval Required For |
|---|---|---|
| Researcher | file_read, git_status, schema_validate, ledger_read | N/A |
| Reviewer | file_read, git_status, schema_validate, ledger_read | N/A |
| Approver | file_read, ledger_read, ledger_write | All ledger writes |
| Admin | file_read, ledger_read | ledger_write (with dual approval) |

## Audit Logging

All tool usage is logged via `schemas/research-lab/audit-event.schema.json`:
- Event type: `access`, `modification`, `validation`
- Actor: Role identifier
- Resource: File or ledger entry
- Outcome: success, failure, blocked

## References

- ADR-0010: MCP boundary tool permission
- MCP_BOUNDARY.md: Host-owned permissions
- MCP_TOOL_PERMISSION_MODEL.md: Detailed permission model
