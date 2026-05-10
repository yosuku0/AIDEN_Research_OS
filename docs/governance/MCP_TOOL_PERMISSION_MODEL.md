# MCP_TOOL_PERMISSION_MODEL

## Purpose

Define MCP tool authorization by agent role and tool category.

## Tool Categories

- read-only: inspect reviewed artifacts and public reference summaries.
- write-capable: create or edit explicitly allowed repository artifacts.
- execution-capable: run commands, tests, simulations, or external-effect operations.

## Permission Matrix

| Agent | read-only | write-capable | execution-capable | Notes |
|---|---|---|---|---|
| Market Analyst | Allowed for reviewed research artifacts | Draft-only research artifacts when scoped | Not allowed | No market execution authority. |
| Coder | Allowed within task context | Allowed only in task allowed_files | Local validation only when approved | Cannot deploy or access secrets. |
| Reviewer | Allowed for all reviewed artifacts | Comments and proposed edits only | Validation only when approved | Cannot approve Human gates. |
| Executor | Future sandbox only | Future sandbox only | Future Firecracker sandbox only | Not implemented in this repository. |

## Minimum Necessary Tools

Each role receives the smallest tool set required for the current approved task. Tool expansion requires ADR update, ledger update, and Human approval.

## Tool Invocation Logging

Logging requirements: trace_id, actor, role, tool_name, tool_category, purpose, policy_basis, approval_reference, input_classification, output_classification, and result.


## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md, research/ledgers/approval-record.md.
