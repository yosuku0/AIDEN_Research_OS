# THREAT_MODEL

## Purpose

Threats include secret exposure, raw artifact promotion, execution boundary bypass, approval spoofing, tool overpermission, model routing overrun, and source-of-truth confusion.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Controls

Stop on hard-ban drift, create incident-record, and require Human review before resume.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, research/ledgers/approval-record.md.
