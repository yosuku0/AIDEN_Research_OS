# EXECUTION_BOUNDARY

## Purpose

Defines the runtime, artifact, Human, release, and forbidden-action boundaries.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Runtime Boundary

The research layer cannot directly trigger execution.

## Artifact Boundary

Only reviewed GitHub artifacts pass to Codex or implementation planning. Raw prompts, raw outputs, raw logs, and local-only material are excluded.

## Human Gate

Merge, capital, allowlist, release, phase gate, and authority changes require Human approval.

## Release Gate

A phase-gate-record entry is required before closing a phase.

## Forbidden Actions

Signing, deploying, approving swaps, bridging, transferring, production writes, wallet access, private key custody, and automatic risk limit changes are forbidden.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, research/ledgers/approval-record.md.
