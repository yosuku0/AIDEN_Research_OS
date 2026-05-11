# AIDEN Research OS - Codex Autonomous Development Package

Complete package for resolving all 7 audit findings and enabling full autonomous development via OpenAI Codex app.

## Version History

| Version | Date | Changes |
|---|---|---|
| V1 | 2026-05-11 | Initial package. Codex stopped due to (a) old forbidden fixture with credential literals, (b) codex-app-package/ untracked directory. |
| V2 | 2026-05-11 | Fixed: forbidden fixture uses abstract markers; .gitignore excludes codex-app-package/; Master Prompt V2 with Phase 2 tasks; 4 new Codex tasks (PR-0021~0024); ADR-0019 for CODEOWNERS exemption. |

## What Codex Already Completed (Branch: codex/pr-0018-ci-hardening)

| # | Task | Status | Evidence |
|---|---|---|---|
| 1 | validate-governance.sh: /tmp removed | DONE | PR #1 |
| 2 | Secret scan: file-path-only output | DONE | PR #1 |
| 3 | forbidden-content.cases.json (abstract markers) | DONE | PR #1 |
| 4 | no-secret.valid.json passes schema | DONE | PR #1 |
| 5 | ADR-0005 / ADR-0011 Risks/Follow-ups differentiated | DONE | PR #1 |
| 6 | safe-config.schema.json 2020-12 pilot migration | DONE | PR #1 |
| 7 | INC-008 recorded (V1 stop condition) | DONE | incident-record.md |

## What Remains (Execute with V2 Prompt)

| ID | Task | Priority | File(s) |
|---|---|---|---|
| R1 | Repository cleanup (.gitignore codex-app-package/) | HIGH | .gitignore |
| R2 | Ledger structure validation CI job | HIGH | governance-ci.yml |
| R3 | APPROVAL_FLOW.md PR review (Human only) | HIGH | PR #1 review |
| R4 | ADR differentiation backfill (15 remaining ADRs) | MEDIUM | docs/adr/ADR-*.md |
| R5 | Pilot schema extension (x- prefix fields) | MEDIUM | safe-config.schema.json |
| -- | CODEOWNERS update (Human only, ADR-0019) | LOW | .github/CODEOWNERS |

## Audit Findings Resolved by This Package

| ID | Severity | Finding | Resolution File |
|---|---|---|---|
| H-001 | CRITICAL | All ARs stuck at "hold" | APPROVAL_FLOW.md + approval-record.md |
| H-002 | HIGH | Documentation-only tests | ADR-0018 + governance-ci.yml |
| H-003 | HIGH | Secret scan leaks to /tmp/logs | validate-governance.sh + governance-ci.yml |
| H-004 | MEDIUM | Schema Draft-07 debt | SCHEMA_EVOLUTION_POLICY.md |
| H-005 | MEDIUM | ADR mechanical copy-paste | ADR_DIFFERENTIATION_GUIDE.md |
| H-006 | MEDIUM | additionalProperties blocks extensions | SCHEMA_EVOLUTION_POLICY.md |
| H-007 | LOW | CODEOWNERS placeholder | ADR-0019 (Human exemption) + CODEOWNERS guide |

## Package Structure

```
codex-app-package/
|-- CODEX_MASTER_PROMPT_V2.md          <-- USE THIS (not V1)
|-- .gitignore                         <-- codex-app-package/ exclusion
|-- docs/
|   |-- adr/
|   |   |-- ADR-0018-executable-test-migration.md
|   |   |-- ADR-0019-codeowners-protection-exemption.md
|   |-- governance/
|       |-- APPROVAL_FLOW.md           <-- +Checklist +Transitions
|       |-- ADR_DIFFERENTIATION_GUIDE.md
|       |-- SCHEMA_EVOLUTION_POLICY.md
|-- research/
|   |-- ledgers/
|       |-- approval-record.md         <-- +criteria_met, +AR-0018~0020
|       |-- decision-log.md            <-- +DL-0018~0020
|       |-- incident-record.md         <-- +INC-001~008
|       |-- phase-gate-record.md       <-- +PG-0018~0020
|       |-- redaction-checklist.md     <-- +RC-0018~0020
|       |-- task-promotion-record.md   <-- +TP-0018~0020
|-- schemas/                           <-- Schema evolution policy applies
|-- scripts/
|   |-- validate-governance.sh         <-- No /tmp, file-paths-only
|-- .github/
|   |-- CODEOWNERS                     <-- +Replacement instructions
|   |-- workflows/
|       |-- governance-ci.yml          <-- +Secure output +Fixture validation
|-- codex/
|   |-- tasks/
|       |-- PR-0018-approval-process-activation.md
|       |-- PR-0019-ci-security-hardening.md
|       |-- PR-0020-executable-test-migration.md
|       |-- PR-0021-repo-cleanup.md          (V2 new)
|       |-- PR-0022-ledger-structure-validation.md (V2 new)
|       |-- PR-0023-adr-differentiation-backfill.md (V2 new)
|       |-- PR-0024-pilot-schema-extension.md (V2 new)
|-- fixtures/
    |-- security/
        |-- secret-manager/
            |-- no-secret.valid.json
            |-- forbidden-content.cases.json   <-- Abstract markers (no real secrets)
```

## Codex App Usage

### Step 1: Clean up repository (Human)

```bash
# Remove codex-app-package/ from tracking if accidentally committed
git rm -r --cached codex-app-package/ 2>/dev/null || true

# Copy .gitignore to repo root
cp codex-app-package/.gitignore .gitignore

# Commit
git add .gitignore
git commit -m "chore: exclude codex-app-package/ from repo"
```

### Step 2: Copy V2 files into repository

```bash
# Copy governance files
cp codex-app-package/docs/governance/APPROVAL_FLOW.md docs/governance/APPROVAL_FLOW.md
cp codex-app-package/docs/governance/ADR_DIFFERENTIATION_GUIDE.md docs/governance/
cp codex-app-package/docs/governance/SCHEMA_EVOLUTION_POLICY.md docs/governance/

# Copy ADR
cp codex-app-package/docs/adr/ADR-0018-executable-test-migration.md docs/adr/
cp codex-app-package/docs/adr/ADR-0019-codeowners-protection-exemption.md docs/adr/

# Copy scripts
cp codex-app-package/scripts/validate-governance.sh scripts/validate-governance.sh

# Copy CI workflow
cp codex-app-package/.github/workflows/governance-ci.yml .github/workflows/governance-ci.yml

# Copy ledgers
cp codex-app-package/research/ledgers/*.md research/ledgers/

# Copy fixtures
cp codex-app-package/fixtures/security/secret-manager/*.json fixtures/security/secret-manager/

# Copy Codex tasks
cp codex-app-package/codex/tasks/*.md codex/tasks/

# Commit
git add .
git commit -m "chore: apply audit fix package V2"
```

### Step 3: Execute with Codex app

1. Open OpenAI Codex app
2. Paste contents of `CODEX_MASTER_PROMPT_V2.md` as the prompt
3. Codex executes R1 -> R2 -> R4 -> R5 in order
4. Review each output before approving next phase

### Step 4: Human-only actions (Codex cannot do these)

| Action | How |
|---|---|
| Review & merge PR #1 | https://github.com/yosuku0/AIDEN_Research_OS/pull/1 |
| Replace @repo-owner in CODEOWNERS | ADR-0019 exemption: create branch, replace, self-review, merge |
| Approve AR-0018~0020 | Update approval-record.md after checklist verification |

## Validation

After all tasks complete:

```bash
bash scripts/validate-governance.sh
# Expected: all checks pass
```

## Safety Design

- 12 Absolute Hard Bans (execution, credentials, deployment prohibited)
- 6 Human Approval Gates (AR approval, CODEOWNERS, ADR status changes)
- 6 Stop Conditions (forbidden files, scope creep, secrets, boundary drift, .gitignore violation, protected files)
- Task dependency graph prevents out-of-order execution
