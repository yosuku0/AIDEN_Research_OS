# HUMAN_APPROVAL_KILL_SWITCH

## Purpose

Kill switch stops workflows on boundary drift, secret exposure, approval spoofing, or execution-adjacent behavior. Restart requires incident closure and Human approval.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Controls

Stop on hard-ban drift, create incident-record, and require Human review before resume.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, research/ledgers/approval-record.md.
