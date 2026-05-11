# ADR-0005: Cloud Local Role Split

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Route high-precision synthesis to cloud models and high-frequency triage to local models; neither receives execution authority.

## Rejected Alternatives

- Cloud-only: rejected because it weakens boundaries, auditability, or Human final approval.
- Local-only: rejected because it weakens boundaries, auditability, or Human final approval.
- Execution-capable inference agents: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- Cloud model provider failure may stall high-precision synthesis tasks if no documented fallback path exists.
- Local model misclassification may route complex synthesis to local inference and degrade research output quality.
- Budget threshold ambiguity may cause either excessive cloud spend or premature workflow holds.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Define concrete budget thresholds before cloud escalation is enabled.
- Validate the local model list against the target workstation constraints before operational use.
- Review cloud provider failover options within the no-execution boundary.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting follow-up rules.
