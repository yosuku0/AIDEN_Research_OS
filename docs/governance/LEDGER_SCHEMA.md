# LEDGER_SCHEMA

## Purpose

Schemas: decision-log DL-XXXX with decision_type, status, owner, linked_adr, linked_codex_task, decision, alternatives, rationale, consequences, rollback_plan. risk-ledger RK-XXXX with risk_class, severity, likelihood, status, trigger, mitigation controls, detection method, residual risk. approval-record AR-XXXX with approval_type, requested_by, approver, approval_scope, linked_pr, linked_phase_gate. redaction-checklist, incident-record, task-promotion-record, open-questions, and phase-gate-record follow schemas/governance.

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
