# HITL_APPROVAL_DESIGN

## Purpose

Define Human approval node placement, actions, resume behavior, timeout handling, escalation, and kill switch integration.

## Human Approval Placement

Human approval nodes are placed before merge, phase gate, allowlist, capital, release, hard-ban modification, and authority changes.

## Approval Actions

Approve proceeds within the named scope. Edit returns to the responsible node. Reject stops or returns to planning. Hold pauses until blockers are resolved.

## Resume After Interruption

Resume requires checkpoint state plus a matching approval-record entry. The resumed workflow must verify requested scope, approver, conditions, and linked artifact identifiers.

## Timeout and Escalation

Timeout moves the workflow to Hold. Escalation routes to Human review and updates open-questions when unresolved blockers remain.

## Emergency Kill Switch

The kill switch stops workflow progression on boundary drift, redaction failure, approval spoofing, secret exposure, or execution-adjacent behavior. Resume requires incident closure and Human approval.


## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md, research/ledgers/approval-record.md.
