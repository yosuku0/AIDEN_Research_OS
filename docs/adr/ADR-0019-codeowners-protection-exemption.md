# ADR-0019: CODEOWNERS Protection Exemption for Audit Fix

## Status

Proposed

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a research/control-plane scaffold, not a trading implementation. Human approval remains final for merge, capital, allowlist, release, phase gate, and authority changes.

The CODEOWNERS file at `.github/CODEOWNERS` is protected by `AGENTS.md` as a governance-critical file. Codex is forbidden from modifying it directly. However, audit finding H-007 (LOW) identified that CODEOWNERS uses the placeholder `@repo-owner` instead of an actual GitHub username or team.

This creates a practical problem: the audit fix cannot be applied by Codex due to the AGENTS.md protection rule, yet leaving the placeholder indefinitely means CODEOWNERS is non-functional (no automatic reviewer assignment on PRs).

## Decision

Create a narrowly scoped exemption for H-007 remediation only. The exemption allows:

1. A Human to create a **dedicated branch** for CODEOWNERS update only
2. The update is **limited to replacing `@repo-owner` with the actual GitHub handle**
3. No other changes to CODEOWNERS paths or rules
4. The change is reviewed and approved by the same Human who makes it (self-approval acceptable for this specific placeholder fix only)

The exemption is **one-time and self-terminating** -- after the placeholder is replaced, AGENTS.md protection resumes fully.

## Rejected Alternatives

- Codex modifies CODEOWNERS: rejected because AGENTS.md explicitly protects this file, and the actual owner identity must be provided by Human
- Leave placeholder indefinitely: rejected because non-functional CODEOWNERS means no automatic reviewer assignment, weakening governance
- Broad exemption for all protected files: rejected because it would undermine AGENTS.md protection across the board

## Consequences

CODEOWNERS will become functional with the actual owner assigned. Automatic reviewer assignment on PRs will work. AGENTS.md protection for other files remains intact.

## Risks

- Incorrect handle: Human may mistype their GitHub handle. Mitigation: verify with `git remote -v` or GitHub profile URL before commit.
- Scope creep: exemption could be used for broader CODEOWNERS changes. Mitigation: ADR explicitly limits to `@repo-owner` replacement only.

## Follow-ups

- Human creates branch, replaces @repo-owner, self-reviews, merges
- Update AR-0019 decision to "approved" with timestamp
- Close INC-007 (CODEOWNERS placeholder) as resolved
- AGENTS.md protection resumes; no further exemptions without new ADR

## Linked Audit Findings

- H-007: LOW - CODEOWNERS placeholder
- INC-007: Recorded in incident-record.md

## Linked Codex Tasks

None - this ADR requires Human action only, Codex does not execute this.
