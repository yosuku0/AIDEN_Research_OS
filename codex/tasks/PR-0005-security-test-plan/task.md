# Security test plan

## task_id
PR-0005-security-test-plan

## title
Security test plan

## status
draft

## human_approval_required
true

## task_class
governance

## risk_level
High

## goal
Complete the docs-only phase artifact set for Security test plan.

## background
Part of AIDEN Research OS, a research/control-plane scaffold and not a trading implementation.

## inputs
CODEX_PROMPT.md summary, SAFETY.md, PRODUCT_BOUNDARY, EXECUTION_BOUNDARY, related ADRs and ledgers.

## in_scope
Allowed governance, system, security, schema, fixture, test specification, ledger, lab README, and task artifacts.

## out_of_scope
Runtime implementation, provider integration, secret custody implementation, package installation, wallet behavior, signer behavior, deployment, approval execution, swap, bridge, transfer, and production write.

## allowed_files
docs/**, research/**, labs/**/README.md, codex/**, .github/**, schemas/**, fixtures/**, tests/**, README.md, SAFETY.md, packages/.gitkeep.

## forbidden_files
.env, .env.*, runtime/**, src/**, apps/**, packages/** except packages/.gitkeep, package manager files, deployment files, wallet files, signer files, provider integration files.

## required_outputs
All phase artifacts named in the master prompt for this task, with cross-references and ledger updates.

## prohibited_work
Do not store credential values or local secret paths. Do not create executable runtime code. Do not grant AI approval, signing, deploy, transfer, bridge, swap, or production-write authority.

## implementation_notes
Use redacted summaries only. Keep market labs as one-of-many research domains. Treat GitHub artifacts as source of truth only after review.

## tests_or_checks
Run artifact existence, required-heading, ADR section, secret-like content, local-path, and forbidden-file checks.

## acceptance_criteria
Required outputs exist, ADRs include required sections, ledgers follow documented schemas, no forbidden files are edited, and Human approval remains required.

## review_checklist
- Product boundary remains explicit.
- Hard bans are unchanged.
- No raw prompt, output, or log is promoted.
- No credential value or local secret path exists.
- Ledger and ADR references are present.

## rollback_plan
Remove or revise affected artifacts through review, update incident-record if needed, and mark the phase gate Hold.
