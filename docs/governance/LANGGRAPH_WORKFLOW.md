# LANGGRAPH_WORKFLOW

## Purpose

StateGraph design uses checkpoints and nodes Supervisor, MarketAnalyst, Coder, Reviewer, HumanApproval. interrupt_before is used for restricted decisions. Conditional edges route approve, edit, reject, and hold. Persistence progresses InMemory to SQLite to Postgres.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Required Headings

Purpose, Boundary, Policy, Procedure, References.

## Policy

Any expansion requires ADR update, ledger update, and Human approval.

## Procedure

Draft artifact, check hard bans, update ledgers, complete review checklist, then request Human gate when applicable.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, research/ledgers/approval-record.md.
