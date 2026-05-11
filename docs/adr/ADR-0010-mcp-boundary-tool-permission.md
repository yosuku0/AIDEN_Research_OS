# ADR-0010: MCP Boundary Tool Permission

## Status

Accepted

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

## Decision

Use host-owned MCP permissions, minimum necessary tools, and explicit logging.

## Rejected Alternatives

- Server-owned authorization: rejected because it weakens boundaries, auditability, or Human final approval.
- Roots as access control: rejected because it weakens boundaries, auditability, or Human final approval.
- Unrestricted tool access: rejected because it weakens boundaries, auditability, or Human final approval.

## Consequences

The repository favors reviewed artifacts, ADRs, ledgers, schemas, fixtures, and task definitions. Runtime implementation and provider integration remain out of scope unless separately approved.

## Risks

- MCP tool definitions may expand into execution-capable operations without matching ADR review.
- Server-side authorization assumptions may conflict with host-owned permission enforcement.
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks.

## Follow-ups

- Maintain an explicit tool allowlist before adding any MCP server implementation.
- Require audit event fields for each approved tool invocation in future MCP tasks.
- Review at phase gates; keep linked ledgers current.
