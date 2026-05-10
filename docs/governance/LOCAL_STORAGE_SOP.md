# LOCAL_STORAGE_SOP

## Purpose

Define local-only raw artifact workspace rules and GitHub promotion boundaries.

## Local-Only Raw Artifact Workspace

Repo-external local workspaces are used for raw prompts, raw model outputs, and raw runtime logs. These materials are not source-of-truth artifacts.

## Quarantine Workspace

Temporary quarantine is used for redaction work files and incident evidence. Quarantine material remains local-only and is reviewed before any redacted summary is created.

## Retention Policy

Retention must be the shortest practical duration. Local raw artifacts and quarantine material must be purgeable after review, incident closure, or artifact promotion.

## GitHub Promotion

GitHub receives redacted summary artifacts only. Promotion requires redaction-checklist review and ledger linkage.


## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md, research/ledgers/approval-record.md.
