# ADR-0001: Product Is AIDEN Research OS

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Accept the Personal AI Research OS / AIDEN Research OS identity and reject Base-only bot framing.

## Rejected Alternatives

- Base-only bot: rejected because it weakens boundaries, auditability, or Human final approval.
- Single-agent monolith: rejected because it weakens boundaries, auditability, or Human final approval.
- Research Lab in bot: rejected because it weakens boundaries, auditability, or Human final approval.
- AIDEN with signing or deploy authority: rejected because it weakens boundaries, auditability, or Human final approval.
- Obsidian or Notion as source of truth: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

Documentation may drift, approval semantics may become ambiguous, and future contributors may confuse market lab scaffolds with execution systems.

## Follow-ups

Review this ADR at phase gates, keep linked ledgers current, and open follow-up tasks only within approved boundaries.
