# Core Package Scaffold

## task_id
PR-0019-core-implementation

## title
Core Package Scaffold — aiden-core Python Package

## status
draft

## human_approval_required
true

## task_class
implementation

## risk_level
High

## goal
Create packages/aiden-core as the root Python package for the AIDEN runtime.
This task creates all submodule stubs, pyproject.toml, conftest.py, and verifies
pip install succeeds. No business logic yet — pure structure and dependency declaration.

## background
All implementation phases (PR-0020 through PR-0025) depend on this package existing.
The package must be installable before any runtime code can be written.
Dependency choices follow TECH_STACK_MATRIX.md.

## in_scope
packages/aiden-core/pyproject.toml
packages/aiden-core/src/aiden/__init__.py
packages/aiden-core/src/aiden/config/__init__.py
packages/aiden-core/src/aiden/config/settings.py        ← Pydantic BaseSettings
packages/aiden-core/src/aiden/workflow/__init__.py
packages/aiden-core/src/aiden/secrets/__init__.py
packages/aiden-core/src/aiden/models/__init__.py
packages/aiden-core/src/aiden/mcp/__init__.py
packages/aiden-core/src/aiden/observability/__init__.py
packages/aiden-core/tests/conftest.py
packages/aiden-core/tests/__init__.py
packages/aiden-core/tests/integration/__init__.py

## out_of_scope
Business logic in any module (stubs only). Provider integration. Secret values.
Wallet, signer, deploy, production-write code (permanently forbidden).

## allowed_files
packages/aiden-core/** (all files)
packages/.gitkeep (may be removed after package exists)
research/ledgers/decision-log.md (DL-0019 entry)

## forbidden_files
.env, .env.*, any file outside packages/

## required_outputs
- pip install -e "packages/aiden-core[dev]" succeeds
- python -m pytest tests/ -v exits 0 (stubs only, no failures)
- python -m ruff check src/ tests/ exits 0

## prohibited_work
No literal API keys, passwords, seed phrases, or private keys anywhere.
No wallet, signing, or execution imports.

## implementation_notes
settings.py must use Pydantic BaseSettings with AIDEN_ prefix.
No field in settings.py may hold a literal credential value.
All credential access must be via KeychainAdapter in aiden.secrets.keychain.
The FakeKeychain class must be in aiden.secrets.keychain for test use.
AIDEN_OBSERVABILITY_ENABLED=false must produce a no-op tracer.

## tests_or_checks
cd packages/aiden-core
pip install -e ".[dev]"
python -m pytest tests/ -v
python -m ruff check src/ tests/
python -m mypy src/aiden/ --ignore-missing-imports

## acceptance_criteria
- All commands above exit 0
- No literal secrets in any file
- FakeKeychain in keychain.py
- AuditEvent dataclass in observability/tracer.py
- ResearchState TypedDict in workflow/graph.py includes session_cost_usd

## review_checklist
- pyproject.toml lists all dependencies from TECH_STACK_MATRIX.md
- No .env file created
- AIDEN_OBSERVABILITY_ENABLED=false tested in conftest.py

## rollback_plan
Delete packages/aiden-core/. Restore packages/.gitkeep.
