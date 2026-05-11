# CI Hardening

## task_id
PR-0018-ci-hardening

## title
CI Hardening — Schema Validation, Secret Scan, Approval Gate

## status
draft

## human_approval_required
true

## task_class
security

## risk_level
High

## goal
Replace the file-existence-only CI with a multi-job governance pipeline that enforces
schema validity, detects secret-like patterns, validates ADR sections, and gates on
approval record status. Create a local mirror script (scripts/validate-governance.sh)
that Codex and human reviewers can run before every commit.

## background
Audit finding CRIT-01: governance-ci.yml only ran `test -f "$file"` for each required
artifact. This provides zero protection against malformed schemas, secret leakage, or
incomplete ADR structures. Any artifact can pass CI as long as it physically exists,
even if it contains credential material or invalid JSON.

## in_scope
.github/workflows/governance-ci.yml replacement with 6-job pipeline:
  1. artifact-existence (extended file list)
  2. schema-validation (check-jsonschema against fixture/schema pairs)
  3. secret-scan (regex patterns for API keys, private keys, PEM headers, local paths)
  4. adr-structure (required ## sections in each ADR file)
  5. approval-status-check (warning if all records are pending)
  6. python-validate (conditional: ruff + mypy + pytest when aiden-core exists)

scripts/validate-governance.sh as local mirror of jobs 1-5.

## out_of_scope
Runtime implementation, package installation, provider integration, secret values.

## allowed_files
.github/workflows/governance-ci.yml
scripts/validate-governance.sh
research/ledgers/decision-log.md (DL-0018 entry)
research/ledgers/risk-ledger.md (RK-0018 entry)
research/ledgers/approval-record.md (AR-0018 entry)

## forbidden_files
.env, .env.*, runtime/**, src/**, apps/**
docs/ (read-only reference)

## required_outputs
- .github/workflows/governance-ci.yml (multi-job, see AGENTS.md §PR-0018)
- scripts/validate-governance.sh (chmod +x, exits 0 on clean repo)
- Ledger entries: DL-0018, RK-0018, AR-0018

## prohibited_work
Do not store credential values. Do not add hardcoded secrets to the secret-scan
pattern list that look like real values. Do not install packages in the script that
are not already declared as dev dependencies.

## implementation_notes
The secret-scan job scans docs/, research/, fixtures/, schemas/, packages/ (not .venv).
Pattern list must not produce false positives on the existing fixture files.
The approval-status-check job is a WARNING, not a hard failure — human gates are
intentionally async and a PR may be open while approval is pending.

## tests_or_checks
bash scripts/validate-governance.sh   # Must exit 0 on this repository
The script must also exit 1 when a test file with a fake secret pattern is introduced.

## acceptance_criteria
- governance-ci.yml has 6 named jobs
- validate-governance.sh exits 0 on a clean repository
- validate-governance.sh exits 1 when any JSON schema file contains invalid JSON
- Secret scan catches patterns matching sk-[a-zA-Z0-9]{20,}
- Python validate job runs when packages/aiden-core/pyproject.toml exists
- Ledger entries DL-0018, AR-0018 added

## review_checklist
- No secrets in the script itself (no test values with real key shapes)
- Pattern list covers all forbidden secret forms from docs/security/THREAT_MODEL.md
- Warning vs error distinction is clear in CI output
- Script is idempotent (can be run multiple times)

## rollback_plan
Revert .github/workflows/governance-ci.yml to previous version. Mark AR-0018 Hold.
Remove scripts/validate-governance.sh. Open incident-record for security regression.
