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

- Product identity may collapse into a single-bot framing, making the control-plane boundary harder to review.
- Base-only naming or examples may imply chain-specific execution authority that the project does not grant.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Review README and product-boundary language whenever new public-facing docs are added.
- Keep Base references subordinate to the broader AIDEN Research OS identity in future artifacts.
- Review at phase gates; keep linked ledgers current.
