# PR-0021: Repository Cleanup

## task_name

Repository Cleanup (codex-app-package exclusion)

## task_description

Resolve INC-008 by ensuring codex-app-package/ directory is excluded from the repository via .gitignore. Remove any tracked files if present.

## boundary_scope

Repository hygiene task. No governance schema or runtime changes.

## allowed_files

- .gitignore

## forbidden_files

- All files under codex-app-package/ (do NOT stage or commit these)
- .github/CODEOWNERS (protected by AGENTS.md)
- Any source code files

## human_approval

TRUE

## required_outputs

- .gitignore contains `codex-app-package/` line
- `git ls-files | grep codex-app-package` returns empty (no tracked files)

## validation_steps

- Run `git ls-files | grep codex-app-package` -- confirm empty output
- Run `git status` -- confirm codex-app-package/ is not listed as staged
- Confirm .gitignore has `codex-app-package/` entry

## incident_trigger

If codex-app-package/ contains files that need to be preserved in the repository, STOP and create incident-record.md entry.

## rollback_plan

1. Remove `codex-app-package/` line from .gitignore
2. If files were removed from tracking, restore with `git checkout HEAD -- codex-app-package/`

## linked_ledger

INC-008 (resolution)
