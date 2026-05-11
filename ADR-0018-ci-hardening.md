# ADR-0018: CI Hardening — Executable Governance Enforcement

## Status

Proposed

## Context

AIDEN Research OS is a Personal AI Research OS and this repository is a
research/control-plane scaffold. The original governance CI (ADR-0001 era) only
verified that required files existed. A Red Team audit (May 2025) identified this as
Critical finding CRIT-01: any file — including one with invalid JSON, credential
material, or missing ADR sections — would pass CI as long as it physically existed.

Separately, finding CRIT-03 noted that all security test specifications were `.md`
documents with no executable counterpart, meaning secret-handling guarantees rested
entirely on human review.

## Decision

Replace the single-job file-existence CI with a six-job governance pipeline:

1. **artifact-existence** — extended required file list including AGENTS.md,
   scripts/validate-governance.sh, and all ledger files.
2. **schema-validation** — check-jsonschema validates fixture files against their
   schemas; all `.json` files in schemas/ and fixtures/ are validated as parseable JSON.
3. **secret-scan** — grep-based scan for API key patterns, PEM headers, JWT shapes,
   and local path leakage across docs/, research/, fixtures/, schemas/, packages/.
4. **adr-structure** — each ADR-*.md must contain `## Status`, `## Context`,
   `## Decision`, `## Consequences`.
5. **approval-status-check** — emits a warning (not a hard failure) when approval
   records are in pending/hold state, preserving the async Human gate design.
6. **python-validate** — conditionally runs ruff, mypy, and pytest when
   packages/aiden-core/pyproject.toml exists.

A local script `scripts/validate-governance.sh` mirrors jobs 1–5 for pre-commit
use by Codex and human reviewers.

## Rejected Alternatives

- Keep existing single-job CI and add comments: rejected because it provides no
  automated enforcement and was already bypassed.
- Use a third-party secret scanning tool (TruffleHog, GitLeaks) as the only defence:
  rejected because it adds external dependency without replacing the need for schema
  and ADR structure validation.
- Hard-fail CI when all approvals are pending: rejected because Human gates are
  intentionally async — a PR can be open and reviewed while its linked approval
  record awaits human sign-off.

## Consequences

- Every PR now runs 6 CI jobs before merge is allowed.
- Invalid JSON in any schema or fixture file blocks CI.
- Credential-like patterns in governed artifacts block CI.
- Codex can run `bash scripts/validate-governance.sh` before every commit to catch
  failures locally.
- The `python-validate` job is conditional so CI remains fast before PR-0019.

## Risks

- Secret scan patterns may produce false positives on existing synthetic fixture data.
  Mitigation: validate patterns against all existing fixtures before merging PR-0018.
- Schema validation with check-jsonschema requires pip install in CI; this adds
  ~15s to CI time. Acceptable.
- ADR section check uses grep; ADR files with unusual heading capitalisation may
  be flagged. Mitigation: normalize all ADR headings before merging.

## Follow-ups

- After PR-0025 (Integration Test Suite) is approved, promote `python-validate`
  from conditional to required.
- Review this ADR at phase gates PR-0021 (OS Keychain) and PR-0025 (Integration).
- Consider adding JSON Schema draft-07 validation for ledger entries once all
  ledgers are converted to JSON format.
