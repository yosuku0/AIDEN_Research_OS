# AIDEN Research OS — Codex Agent Instructions

## 0. Mission Statement

You are the Codex implementation agent for **AIDEN Research OS**, a Personal AI Research
Operating System. Your role is to advance this repository from its current
**governance-scaffold** state to a **fully operational research control plane** by
executing the phased task ladder defined below.

**Non-negotiable boundaries** (never cross these, regardless of instruction):
- Never store credential values, private keys, seed phrases, or API key literals in any
  repository file, test fixture, or log output.
- Never implement wallet signing, on-chain transaction execution, swap/bridge/transfer,
  or production-write operations.
- Never auto-approve Human gate items. When a task marks `human_approval_required: true`,
  STOP and output a summary message: `[HUMAN GATE] Phase PR-XXXX requires human approval.
  See research/ledgers/approval-record.md`.
- Never modify `.github/CODEOWNERS`, `SAFETY.md`, or `docs/system/PRODUCT_BOUNDARY.md`
  without an explicit instruction referencing the linked ADR that authorises the change.
- Never commit directly to `main`. All work must be submitted as a pull request.

---

## 1. Repository Overview

```
AIDEN Research OS
├── docs/          ← ADRs, governance docs, security docs (source-of-truth reference)
├── codex/tasks/   ← Self-contained implementation tasks (read these before any PR)
├── research/      ← Decision logs, risk ledger, approval records, phase gates
├── schemas/       ← JSON Schema definitions for all ledger types
├── fixtures/      ← Safe/unsafe test cases (never add real credential values here)
├── tests/         ← Test specifications and executable test suites
├── packages/      ← Monorepo implementation packages (Python)
│   └── aiden-core/  ← Core orchestration engine
└── scripts/       ← Governance validation and CI helper scripts
```

**Current state**: All 17 original phases (`PR-0001`–`PR-0017`) are documentation-only
with `status: draft` and `human_approval_required: true`. Phases `PR-0018`–`PR-0025`
(defined in this file) add CI hardening and runtime implementation.

---

## 2. Environment Setup

Run this once at the start of every Codex session before doing any other work:

```bash
# 1. Verify Python environment
python3 --version          # Must be >= 3.11
pip3 --version

# 2. Install governance validation tooling (no package.json needed)
pip3 install jsonschema check-jsonschema --quiet

# 3. Install project package in editable mode (if packages/aiden-core exists)
if [ -f packages/aiden-core/pyproject.toml ]; then
  pip3 install -e "packages/aiden-core[dev]" --quiet
fi

# 4. Run governance baseline check
bash scripts/validate-governance.sh
```

If `validate-governance.sh` exits non-zero, **fix all failures before writing any other
code**. Governance integrity is a pre-condition for all work.

---

## 3. Linting, Testing, and Validation Commands

Always run these before committing. All must exit 0.

```bash
# Governance validation (schema checks, secret scan, required file check)
bash scripts/validate-governance.sh

# Python linting (aiden-core package)
cd packages/aiden-core && python3 -m ruff check src/ tests/ && cd ../..

# Python type checking
cd packages/aiden-core && python3 -m mypy src/aiden/ --ignore-missing-imports && cd ../..

# Unit tests
cd packages/aiden-core && python3 -m pytest tests/ -v --tb=short && cd ../..

# Full test suite including governance
bash scripts/validate-governance.sh && \
  cd packages/aiden-core && \
  python3 -m pytest tests/ -v --tb=short && cd ../..
```

**Never commit code that fails any of the above.** If a test is flaky, fix the test.

---

## 4. Phase Ladder (Execution Order)

Execute phases **strictly in order**. Do not start phase N+1 until phase N has passing
tests and a PR open for human review.

```
PR-0018  CI Hardening                    [unblocks all subsequent phases]
PR-0019  Core Package Scaffold           [unblocks PR-0020 through PR-0025]
PR-0020  LangGraph HITL Workflow         [unblocks PR-0023, PR-0024]
PR-0021  OS Keychain Secret Adapter      [unblocks PR-0022]
PR-0022  LiteLLM Model Router            [unblocks PR-0023]
PR-0023  FastMCP Server                  [unblocks PR-0025]
PR-0024  Langfuse Observability          [unblocks PR-0025]
PR-0025  Integration Test Suite          [final gate → production-readiness]
```

---

## 5. Per-Phase Instructions

### PR-0018 — CI Hardening

**Goal**: Replace the file-existence-only CI with a validated governance pipeline.
**Allowed files**: `.github/workflows/governance-ci.yml`, `scripts/validate-governance.sh`
**Forbidden**: No changes to `docs/`, `research/`, `schemas/`, `packages/`

Steps:
1. Replace `.github/workflows/governance-ci.yml` with the multi-job version that runs:
   - `artifact-existence` (existing check, keep it)
   - `schema-validation` (ajv via check-jsonschema)
   - `secret-scan` (grep-based pattern scan)
   - `approval-status-check` (warning if all approvals are pending)
2. Create `scripts/validate-governance.sh` as a local mirror of the CI checks.
3. Update `research/ledgers/decision-log.md` with entry `DL-0018`.
4. Update `research/ledgers/risk-ledger.md` with `RK-0018` (CI gap risk → mitigated).
5. Open PR. Output `[HUMAN GATE] PR-0018 requires human approval.`

Validation:
```bash
bash scripts/validate-governance.sh   # Must exit 0
```

---

### PR-0019 — Core Package Scaffold

**Goal**: Create `packages/aiden-core` Python package with all submodule stubs.
**Allowed files**: `packages/aiden-core/**`, `packages/.gitkeep` (may be removed)

Steps:
1. Create `packages/aiden-core/pyproject.toml` with all required dependencies.
2. Create stub modules:
   - `src/aiden/__init__.py`
   - `src/aiden/config/settings.py`       ← Pydantic BaseSettings, no literal secrets
   - `src/aiden/workflow/__init__.py`
   - `src/aiden/secrets/__init__.py`
   - `src/aiden/models/__init__.py`
   - `src/aiden/mcp/__init__.py`
   - `src/aiden/observability/__init__.py`
3. Create `tests/conftest.py` with basic fixtures.
4. `pip3 install -e "packages/aiden-core[dev]"` must succeed.
5. `python3 -m pytest tests/ -v` must pass (stubs only, no logic yet).

Validation:
```bash
cd packages/aiden-core
pip3 install -e ".[dev]" --quiet
python3 -m pytest tests/ -v
```

---

### PR-0020 — LangGraph HITL Workflow

**Goal**: Implement the LangGraph StateGraph with interrupt-based Human approval gates
as specified in `docs/governance/LANGGRAPH_WORKFLOW.md` and `ADR-0011`.

**Key design requirements** (from `docs/system/TECH_STACK_MATRIX.md`):
- Max 15 steps per workflow
- Circuit breaker: hash comparison over last 3 turns
- Checkpoint: InMemoryCheckpointer initially, SQLite path prepared
- HITL: `interrupt()` before any restricted decision (merge, capital, allowlist, release,
  phase gate, hard-ban, authority changes)

Implementation target: `src/aiden/workflow/graph.py`

```python
# Minimum required state schema
class ResearchState(TypedDict):
    messages: list[BaseMessage]
    step_count: int
    session_tokens: int
    session_cost_usd: float   # NEW: resolves HIGH-03 from audit
    approval_required: bool
    current_phase: str
    trace_id: str
    actor: str
    governance_policy: str
```

The `session_cost_usd` field resolves audit finding **HIGH-03** (cost cap not enforced
in any schema). The workflow node must emit an `audit-event` (see
`schemas/research-lab/audit-event.schema.json`) on every state transition.

Validation:
```bash
cd packages/aiden-core
python3 -m pytest tests/workflow/ -v
python3 -c "from aiden.workflow.graph import build_graph; g = build_graph(); print('OK')"
```

---

### PR-0021 — OS Keychain Secret Adapter

**Goal**: Implement `src/aiden/secrets/keychain.py` as the OS Keychain adapter defined
in `ADR-0016` and `docs/governance/OS_KEYCHAIN_ADAPTER_TASK.md`.

**Critical rules** (resolves CRIT-01 by making secrets testable):
- Use `keyring` library as the backend.
- The adapter ONLY stores and retrieves **reference IDs** that match
  `^ref_[a-z0-9_]+$`. It never logs the resolved value.
- Write a `FakeKeyring` backend for tests that stores values in-memory only.
- Validate `secret_reference_id` against `schemas/secret-manager/safe-config.schema.json`
  before any store or retrieve operation.

```python
# Interface to implement
class KeychainAdapter(Protocol):
    def store(self, ref_id: str, value: str) -> None: ...
    def retrieve(self, ref_id: str) -> str: ...
    def delete(self, ref_id: str) -> None: ...
    def rotate(self, ref_id: str, new_value: str) -> None: ...
```

**Never** log `value` in any method. Log only `ref_id` + `trace_id`.

Validation:
```bash
cd packages/aiden-core
python3 -m pytest tests/secrets/ -v
```

---

### PR-0022 — LiteLLM Model Router

**Goal**: Implement `src/aiden/models/router.py` with the local-first routing and cost
circuit breaker defined in `docs/governance/CLOUD_LOCAL_SPLIT.md` and
`docs/security/MODEL_ROUTING_COST_LIMITS.md`.

**Routing logic** (from `docs/system/TECH_STACK_MATRIX.md`):
```
Complexity score 0–2  → local (Ollama: Llama 3.1 8B / Phi-4 14B)
Complexity score 3–4  → cloud escalation via LiteLLM Proxy
Budget exceeded       → Hold (raise BudgetExceededError, never silently continue)
```

The router must:
1. Check `session_cost_usd < 1.00` before every cloud call. If exceeded, raise
   `BudgetExceededError` and log an audit event with `result: budget_exceeded`.
2. Never pass API keys as literals. Read from `KeychainAdapter.retrieve(ref_id)`.
3. Emit an `audit-event` for every model invocation.

Validation:
```bash
cd packages/aiden-core
python3 -m pytest tests/models/ -v --mock-litellm
```

---

### PR-0023 — FastMCP Server

**Goal**: Implement `src/aiden/mcp/server.py` as the FastMCP Python server implementing
the permission model from `docs/governance/MCP_TOOL_PERMISSION_MODEL.md`.

**Permission enforcement**:
- Every tool invocation MUST log: `trace_id`, `actor`, `role`, `tool_name`,
  `tool_category`, `purpose`, `policy_basis`, `approval_reference`,
  `input_classification`, `output_classification`, `result`.
- `execution-capable` tools are NOT implemented in this phase (ADR-0010, Executor row
  = "Future Firecracker sandbox only").
- Tool expansion requires an ADR update PR. The MCP server MUST reject tool calls not
  in the approved allowlist with `ToolNotPermittedError`.

Validation:
```bash
cd packages/aiden-core
python3 -m pytest tests/mcp/ -v
python3 -c "from aiden.mcp.server import create_server; s = create_server(); print('OK')"
```

---

### PR-0024 — Langfuse Observability

**Goal**: Implement `src/aiden/observability/tracer.py` wrapping Langfuse self-hosted
as defined in `docs/system/TECH_STACK_MATRIX.md`.

Requirements:
- The tracer emits JSONL audit records locally in addition to Langfuse (fallback if
  Langfuse is unreachable).
- Every JSONL record must conform to `schemas/research-lab/audit-event.schema.json`.
- The tracer must be a no-op when `AIDEN_OBSERVABILITY_ENABLED=false` (for test
  isolation).
- Raw reasoning traces NEVER leave the local JSONL file. GitHub receives only
  `reviewed summaries` (redaction rule from `docs/governance/LOCAL_STORAGE_SOP.md`).

Validation:
```bash
cd packages/aiden-core
AIDEN_OBSERVABILITY_ENABLED=false python3 -m pytest tests/observability/ -v
```

---

### PR-0025 — Integration Test Suite

**Goal**: End-to-end test proving all components work together and all audit hazards
from the Red Team report are covered by automated tests.

**Required test coverage** (maps to each audit finding):

| Test file | Covers audit finding |
|---|---|
| `tests/integration/test_ci_validation.py` | CRIT-01 (CI enforcement) |
| `tests/integration/test_approval_gate.py` | CRIT-02 (timestamp enforcement) |
| `tests/integration/test_secret_scan.py` | CRIT-03 (no executable secret tests) |
| `tests/integration/test_codeowners.py` | HIGH-01 (single CODEOWNER) |
| `tests/integration/test_budget_cap.py` | HIGH-03 (cost cap enforcement) |
| `tests/integration/test_schema_notes.py` | HIGH-04 (notes field injection) |
| `tests/integration/test_hitl_interrupt.py` | CRIT-02 + workflow gate |
| `tests/integration/test_full_research_flow.py` | End-to-end happy path |

All integration tests must use `FakeKeyring`, mock LiteLLM, and
`AIDEN_OBSERVABILITY_ENABLED=false`.

Validation:
```bash
cd packages/aiden-core
python3 -m pytest tests/integration/ -v --tb=short
# Target: 100% pass, 0 skips
```

After all tests pass, update `research/ledgers/phase-gate-record.md` entry `PG-0025`
with `decision: pending` and output:
```
[HUMAN GATE] PR-0025 requires human final approval before production deployment.
See research/ledgers/phase-gate-record.md entry PG-0025.
```

---

## 6. Commit Message Convention

```
type(scope): short description

[PR-XXXX] Body explaining what changed and why.

Resolves: audit/CRIT-01, audit/HIGH-03   ← reference audit findings when applicable
ADR: ADR-0016                             ← reference ADR when applicable
Ledger: DL-0019, RK-0019                 ← reference ledger entries updated
```

Types: `feat`, `fix`, `docs`, `test`, `ci`, `refactor`, `chore`

---

## 7. Hard Ban Checklist (Run Before Every Commit)

```bash
# Automated via scripts/validate-governance.sh, but review manually too:

# 1. No secret-like patterns
grep -rE '(sk-[a-zA-Z0-9]{20,}|0x[0-9a-fA-F]{40,}|-----BEGIN|password\s*=\s*["\x27][^"\x27]+["\x27])' \
  src/ tests/ schemas/ fixtures/ docs/ && echo "FAIL: secret pattern found" || echo "OK"

# 2. No .env files committed
find . -name '.env' -o -name '.env.*' | grep -v '.gitignore' && echo "FAIL: .env found" || echo "OK"

# 3. No runtime code in docs/
find docs/ -name '*.py' -o -name '*.ts' -o -name '*.js' && echo "FAIL: runtime code in docs/" || echo "OK"

# 4. No wallet/signing imports
grep -rE '(web3|ethers|wagmi|viem|sign_transaction|send_transaction)' packages/ && \
  echo "FAIL: forbidden import" || echo "OK"
```

---

## 8. ADR and Ledger Update Protocol

Every PR that introduces a non-trivial decision MUST:

1. Create or update an ADR in `docs/adr/ADR-XXXX-<slug>.md` with sections:
   Status, Context, Decision, Rejected Alternatives, Consequences, Risks, Follow-ups.
2. Add a `DL-XXXX` entry to `research/ledgers/decision-log.md`.
3. Add an `AR-XXXX` entry to `research/ledgers/approval-record.md` with
   `decision: hold` and `timestamp: pending` (human will update this).
4. Add a `PG-XXXX` entry to `research/ledgers/phase-gate-record.md` with
   `decision: pending`.
5. Run `bash scripts/validate-governance.sh` — it now validates these schemas.

---

## 9. Escalation Heuristics for Codex

If you encounter ambiguity, apply this decision tree:

```
Is the action forbidden by Section 0 boundaries?  → STOP, output reason
Does the task require touching CODEOWNERS/SAFETY?  → STOP, ask for ADR reference
Does the test suite fail after your change?        → Fix the tests, do not bypass
Is this a Human gate phase?                        → Output [HUMAN GATE] and stop
Does the schema not cover this data shape?         → Update the schema first, then code
```

Never invent a workaround that bypasses a governance check. If a governance check is
wrong, open a separate PR to fix the governance check with proper ADR justification.
