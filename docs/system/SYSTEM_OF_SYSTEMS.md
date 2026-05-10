# SYSTEM_OF_SYSTEMS

## Purpose

Defines components, interface contracts, approval boundaries, failure domains, and audit surface.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Components

Human Final Approver, Research Control Plane, AIDEN Runtime, Cloud AI, Local AI, GitHub Artifact Layer, Codex, Market Labs, Audit and Review.

## Interface Contracts

Research questions become reviewed artifacts. Codex receives self-contained tasks. AIDEN routes work and queues approvals but cannot approve or execute.

## Approval Boundaries

Human approval is required for merge, capital, allowlist, release, phase gate, hard-ban, and authority changes.

## Failure Domains

Artifact failure, boundary failure, redaction failure, authority failure, cost failure, and source-of-truth confusion.

## Audit Surface

ADRs, ledgers, task definitions, issue forms, pull request templates, review records, schemas, and fixtures.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, research/ledgers/approval-record.md.
