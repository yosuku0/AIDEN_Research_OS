# CREDENTIAL_ROTATION_SOP

## Purpose

Define credential rotation procedures without implementing credential rotation runtime.

## Rotation Triggers

Rotation triggers include time-based rotation, incident-based rotation, exposure-suspected rotation, owner-change rotation, and provider-policy rotation.

## Procedures by Credential Type

- API key: Human requests rotation, owner rotates outside the repository, reviewer verifies metadata-only references and absence of values.
- Token: Human confirms scope, owner revokes old token and creates replacement outside the repository, reviewer checks audit records.
- Local reference: owner updates metadata-only reference labels and verifies no local secret path is stored.

## Human Approval Requirements

Human approval is required for incident-based rotation, production credential rotation, boundary changes, and rotations affecting release or allowlist posture.

## Verification Steps

Verify revocation, replacement scope, least privilege, ledger update, and absence of credential values or local secret paths in artifacts.

## Rollback Procedures

Rollback never restores exposed material. If rollback is needed, create a new credential outside the repository and record a new decision.


## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md, research/ledgers/approval-record.md.
