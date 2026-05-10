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

Documentation may drift, approval semantics may become ambiguous, and future contributors may confuse market lab scaffolds with execution systems.

## Follow-ups

Review this ADR at phase gates, keep linked ledgers current, and open follow-up tasks only within approved boundaries.
