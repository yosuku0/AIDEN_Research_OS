# LOCAL_ARTIFACT_STORAGE_BOUNDARY

## Purpose

Define local artifact storage targets, retention posture, purge requirements, and GitHub promotion rules.

## Storage Target Definitions

Raw prompt workspace, raw output workspace, runtime log workspace, redaction workspace, and incident evidence workspace are local-only and repo-external.

## Retention Posture

Retention posture is shortest practical local retention. Raw material is kept only long enough for review, redaction, incident handling, or Human-directed analysis.

## Purge Requirements

Purge requirements apply to all local raw artifacts and quarantine workspaces. Purge must be possible after review or incident closure.

## GitHub Promotion Rules

GitHub promotion is redacted only. Raw prompts, raw model outputs, raw runtime logs, secret material, and local secret paths are never promoted.


## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md, research/ledgers/approval-record.md.
