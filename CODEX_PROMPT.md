# AIDEN Research OS — Unified Master Prompt for Codex App
## All Development Phases Batch Execution (RS-00 through RS-17 + Architecture)

---

# SECTION 1: SYSTEM CONTEXT

## 1.1 Product Identity

You are building the **AIDEN Research OS** — a Personal AI Research Operating System.

- **Product umbrella**: Personal AI Research OS
- **Operational name**: AIDEN Research OS
- **Implementation name**: base-ai-research-lab (research control plane / market-lab implementation)
- **Repository type**: research/control-plane scaffold — NOT a trading implementation
- **Repository topology**: monorepo (initial; future split candidate but not yet)
- **Source of Truth**: GitHub (approved artifacts only)
- **Human**: Final approver for all merge, capital, allowlist, release, and phase gate decisions
- **AIDEN role**: runtime substrate / orchestrator — NOT a signer, deployer, or execution authority

## 1.2 System-of-Systems Architecture

```
Human Final Approver
    ↕ (research questions, approvals, capital judgments)
Research Control Plane
    ↓
AIDEN Runtime (orchestrator)
    ↓
├── Cloud AI (high-precision, high-cost inference)
├── Local AI (high-frequency, low-cost processing)
└── GitHub Artifact Layer (reviewed Source of Truth)
    ↓
    ├── Codex (artifact-driven implementation worker)
    └── Market Labs
        ├── Prediction Market Lab
        ├── Perp DEX Lab
        └── Base DEX Lab (one-of-many market domains)
    ↓
Audit and Review
    ↕
Human Final Approver → Minimal Execution Kernel (future, NOT in scope)
```

## 1.3 Actor Responsibility Matrix

| actor | primary role | can do | cannot do | human approval needed |
|---|---|---|---|---|
| AIDEN | orchestration / runtime policy | plan, route, tool dispatch, approval queue, artifact assist | private key, signing, deploy, approve, swap, production write | risky action, authority change, execution-adjacent judgment |
| Cloud AI | high-precision inference | deep research, counter-evidence, policy draft, architecture review | execution authority, secret management, final approval | sensitive data sent to cloud |
| Local AI | high-frequency processing | summarization, classification, routing support, offline fallback | authority exercise, irreversible action alone | crossing sensitive boundary |
| GitHub | reviewed SoT | docs, ADRs, tasks, PRs, review history, workflow surfaces | raw transcript, API keys, .env, raw runtime log canonicalization | policy/ADR/task promotion/merge |
| Codex | artifact-driven implementation worker | docs/scaffold editing, checks execution within task scope | final approval, capital judgment, secret handling, execution authority | task execution approval |
| Human | final approver | merge, capital, allowlist, release, phase gate | nothing — holds final responsibility | always for boundary/authority changes |

## 1.4 Absolute Hard Bans (NEVER violate)

1. NEVER give AIDEN/Cloud AI/Local AI/Codex private keys, seeds, API keys, production credentials, signing authority
2. NEVER implement deploy/approve/swap/bridge/transfer/production write in any RS phase
3. NEVER connect research output directly to execution without GitHub artifact + review + Human gate
4. NEVER use GitHub for raw prompt/raw transcript/raw output/raw local log/secret backup
5. NEVER use public Base endpoint as production default
6. NEVER use Base-only branding for product identity
7. NEVER allow AI to auto-modify allowlist or risk limits
8. NEVER store credential values or local secret paths in GitHub
9. NEVER implement secret manager runtime, OS keychain adapter, local encrypted vault before approved
10. NEVER add runtime code, CI changes, package installs, provider integrations without explicit approval

---

# SECTION 2: EXECUTION PHASES

Execute ALL phases in order. Each phase generates specific artifacts. Do NOT skip phases.

---

## PHASE 0: Repository Scaffold (PR-0001)
**Goal**: Create the complete directory structure and root governance files.

**Allowed files**:
- README.md, SAFETY.md
- docs/system/*.md
- docs/governance/*.md
- docs/adr/ADR-0001*.md through ADR-0004*.md
- research/**/README.md, research/ledgers/*.md
- labs/**/README.md
- codex/templates/*.md, codex/tasks/PR-0001*/task.md
- .github/CODEOWNERS, .github/PULL_REQUEST_TEMPLATE.md, .github/ISSUE_TEMPLATE/*.md, .github/workflows/*.yml
- packages/.gitkeep

**Required outputs**:

1. **README.md** with:
   - Product identity: Personal AI Research OS / AIDEN Research OS
   - This is a research/control-plane scaffold, not a trading implementation
   - Architecture overview (system-of-systems)
   - Quick start for contributors
   - Safety constraints summary
   - Links to key docs

2. **SAFETY.md** with hard bans listed in Section 1.4 above

3. **docs/system/PRODUCT_BOUNDARY.md**:
```markdown
# PRODUCT_BOUNDARY
## Product identity
- Product umbrella: Personal AI Research OS
- Operational name: AIDEN Research OS
- Lab implementation name: base-ai-research-lab
- This repository is a research/control-plane scaffold and not a trading implementation.
## What the product is
- A research control plane that turns research questions into: specifications, ADRs, Codex tasks, audit inputs, knowledge updates
## What the product is not
- Not a single autonomous trading bot
- Not a Base-only product
- Not a wallet/signing system
- Not a deployment engine
- Not a production-write agent
## In scope
- research, system design, artifact generation, audit routing, market-lab orchestration, knowledge accumulation
## Out of scope
- private key handling, transaction signing, approve/swap/bridge/transfer, deploy, production write, market-specific live execution logic
## Boundaries
- Research Lab sits above AIDEN runtime
- GitHub is Source of Truth
- Human is final approver
- Base DEX Lab is one market domain among several labs
## Safety constraints
- No secrets in repository
- No direct research-to-execution shortcut
- No authority transfer to AIDEN/Cloud AI/Local AI/Codex
## Success metrics
- % of research outputs converted into reusable artifacts
- clarity of boundaries
- auditability of decisions
```

4. **docs/system/SYSTEM_OF_SYSTEMS.md** with components, interface contracts, approval boundaries, failure domains, and audit surface (use architecture from Section 1.2)

5. **docs/adr/ADR-0001-product-is-aiden-research-os.md**: Status=Accepted, Context, Decision, Rejected alternatives (Base-only bot, single-agent monolith, Research Lab in bot, AIDEN with signing/deploy authority, Obsidian/Notion as SoT), Consequences, Risks, Follow-ups

6. **docs/adr/ADR-0002-github-is-source-of-truth.md**: GitHub as SoT decision with justification from protected branches, CODEOWNERS, issue forms, workflow files

7. **docs/adr/ADR-0003-initial-monorepo-topology.md**: Monorepo decision with rejected alternatives (multi-repo, hybrid)

8. **docs/adr/ADR-0004-market-labs-directory-is-labs.md**: labs/ directory structure decision

9. **docs/governance/SOURCE_OF_TRUTH.md**: Canonical artifact policy
10. **docs/governance/REPOSITORY_TOPOLOGY.md**: Repo shape and directory responsibilities
11. **docs/governance/ARTIFACT_TAXONOMY.md**: Classification of all artifact types
12. **docs/governance/APPROVAL_FLOW.md**: Human approval process with approval-record.md as canonical
13. **docs/governance/DEEP_RESEARCH_FLOW.md**: Research → design → Codex task → implementation → audit → knowledge cycle
14. **docs/governance/RUNBOOK.md**: Operational procedures

15. **research/ledgers/**: Create all ledger files with initial schemas:
    - research-ledger.md, evidence-ledger.md, risk-ledger.md, decision-log.md
    - approval-record.md (empty template with schema)
    - redaction-checklist.md, incident-record.md
    - task-promotion-record.md, open-questions.md

16. **labs/base-dex-lab/README.md**, labs/prediction-market-lab/README.md, labs/perp-dex-lab/README.md: Placeholder READMEs identifying each as one-of-many market domains

17. **.github/CODEOWNERS**: Root repo owner as code owner for all governance paths
18. **.github/PULL_REQUEST_TEMPLATE.md**: PR template with governance checklist
19. **.github/ISSUE_TEMPLATE/**: research_sprint.yml, codex_task.yml, bug_report.yml, feature_request.yml
20. **.github/workflows/governance-ci.yml**: Workflow to validate artifact existence

21. **codex/templates/task-template.md**: Reusable task template with all required fields
22. **codex/templates/pr-audit-template.md**: PR audit checklist template
23. **codex/tasks/PR-0001-root-scaffold/task.md**: Self-contained task definition

---

## PHASE 1: Cloud AI × Local AI Role Split (PR-0002)
**Goal**: Define the precise division of labor between cloud and local inference.

**Inputs**: RS-02 documents, Japanese architecture design tech stack matrix

**Required outputs**:
1. **docs/governance/CLOUD_LOCAL_SPLIT.md** with:
   - Cloud AI scope: Deep Research, counter-evidence, policy drafting, architecture review, long-form synthesis, ADR draft
   - Local AI scope: summarization, classification, routing support, offline fallback, triage
   - Routing logic: Local first, Cloud escalates, neither has execution authority
   - Model references: Ollama (Llama 3.1 8B, Qwen2.5 7-14B, Phi-4 14B) for local; Claude/GPT for cloud escalation
   - Cost optimization: LiteLLM Proxy as unified exit point with budget limits
   - Hardware constraints: RTX 4070 Ti 12GB → effective ~10.8GB VRAM

2. **docs/adr/ADR-0005-cloud-local-role-split.md**: Formal ADR recording the decision

3. **docs/system/TECH_STACK_MATRIX.md**: Complete tech stack selection matrix with:
   - Orchestration: LangGraph (primary), CrewAI (prototyping only)
   - Local inference: Ollama (primary), vLLM (future scale)
   - MCP implementation: FastMCP (Python, standard)
   - Hybrid routing: LiteLLM Proxy
   - HITL: LangGraph interrupt()
   - Sandboxing: Firecracker microVM (future)
   - Observability: Langfuse (self-hosted)

4. Update **research/ledgers/decision-log.md** with DL-0002 entry
5. Update **research/ledgers/open-questions.md** with follow-up items

---

## PHASE 2: Governance Ledger Schema (PR-0003)
**Goal**: Establish the complete governance ledger system with schemas and redaction workflow.

**Inputs**: RS-03 documents, RS-03A artifact sheet

**Required outputs**:
1. **docs/governance/LEDGER_SCHEMA.md** with schemas for:
   - decision-log (DL-XXXX): decision_type, status, owner, linked_adr, linked_codex_task, decision statement, alternatives, rationale, consequences, rollback_plan
   - risk-ledger (RK-XXXX): risk_class, severity, likelihood, status, trigger, mitigation controls, detection method, residual risk
   - approval-record (AR-XXXX): approval_type, requested_by, approver, approval_scope, linked_pr, linked_phase_gate
   - redaction-checklist: pre-promotion verification steps
   - incident-record: incident classification, response steps, closure criteria
   - task-promotion-record: research-to-Codex promotion criteria
   - open-questions: question, status, blocker, related_adr
   - phase-gate-record: go/no-go/hold decisions with justification

2. **docs/governance/REDACTION_WORKFLOW.md**:
   - Redaction required before GitHub promotion
   - Raw prompts, raw model outputs, raw runtime logs → redacted summary only
   - Redaction failure → immediate stop, artifact isolation, incident-record creation
   - Local-only data never promoted to SoT in raw form

3. **schemas/governance/**: JSON schemas for all ledger types
4. **docs/adr/ADR-0006-governance-ledger-schema.md**
5. Update **research/ledgers/** with initial entries for all ledger types
6. **codex/tasks/PR-0003-governance-ledger/task.md**

---

## PHASE 3: Runtime Integration Boundary (PR-0004)
**Goal**: Define AIDEN runtime boundaries and security-test handoff.

**Inputs**: RS-04 documents, RS-04B, RS-04C

**Required outputs**:
1. **docs/system/EXECUTION_BOUNDARY.md**:
   - Runtime boundary: research layer cannot directly trigger execution
   - Artifact boundary: only reviewed artifacts pass to Codex
   - Human gate: merge/capital/allowlist/release require human approval
   - Release gate: phase gate approval required
   - Forbidden actions: signing, deploying, approving swaps, production write

2. **docs/adr/ADR-0007-runtime-integration-boundary.md**
3. **docs/adr/ADR-0008-aiden-runtime-boundary.md**
4. **docs/security/HARDENING_POSTURE.md**: Security hardening baseline
5. **docs/security/THREAT_MODEL.md**: Research lab threat model
6. **docs/security/HUMAN_APPROVAL_KILL_SWITCH.md**: Kill switch design
7. **docs/security/PRODUCTION_EXECUTION_PROHIBITION.md**: Production execution ban
8. **docs/security/MODEL_ROUTING_COST_LIMITS.md**: Token budget and cost limits
9. **docs/security/NETWORK_RPC_ALLOWLIST.md**: Allowed RPC endpoints
10. **docs/security/SIMULATION_EVIDENCE_FORMAT.md**: Evidence format for simulations
11. **docs/security/AUDIT_LEDGER.md**: Audit trail requirements
12. Update ledgers
13. **codex/tasks/PR-0004-runtime-boundary/task.md**

---

## PHASE 4: Security Test Plan (PR-0005)
**Goal**: Create comprehensive security test plan for the research lab.

**Inputs**: RS-05 documents, RS-05B artifact sheet

**Required outputs**:
1. **docs/governance/RESEARCH_LAB_SECURITY_TEST_PLAN.md**:
   - Security test scope and methodology
   - Test categories: artifact governance, approval boundary, secret handling, execution isolation
   - Test fixtures: safe and unsafe approval scenarios
   - Validation criteria for each test

2. **schemas/research-lab/**: audit-event.schema.json, simulation-result.schema.json, evidence-bundle.schema.json
3. **fixtures/governance/**: safe-approval-fixtures.json, unsafe-approval-fixtures.json
4. **fixtures/research-lab/safe/** and **fixtures/research-lab/unsafe/**: Test scenarios
5. **docs/adr/ADR-0009-research-lab-security-test-plan.md**
6. **tests/security/**: Security test specifications (markdown, no executable code)
7. **tests/governance/**: Governance validation test specs
8. Update ledgers
9. **codex/tasks/PR-0005-security-test-plan/task.md**

---

## PHASE 5: MCP Boundary and Tool Permission Model (PR-0006)
**Goal**: Define MCP architecture boundaries and tool authorization.

**Inputs**: RS-06 documents, RS-06B artifact sheet

**Required outputs**:
1. **docs/governance/MCP_BOUNDARY.md**:
   - MCP host-client-server separation
   - Host owns permissions, consent, connection lifecycle, authorization decisions
   - Tool allowlisting by agent role
   - Roots are advisory only, not access control
   - No secret passage through MCP

2. **docs/governance/MCP_TOOL_PERMISSION_MODEL.md**:
   - Permission matrix by agent (Market Analyst, Coder, Reviewer, Executor)
   - Tool categories: read-only, write-capable, execution-capable
   - Each agent gets minimum necessary tools
   - Tool invocation logging requirements

3. **docs/adr/ADR-0010-mcp-boundary-tool-permission.md**
4. Update ledgers
5. **codex/tasks/PR-0006-mcp-boundary/task.md**

---

## PHASE 6: LangGraph Workflow and HITL Approval (PR-0007)
**Goal**: Design LangGraph workflows with Human-in-the-Loop approval gates.

**Inputs**: RS-07 documents, RS-07A, RS-07B, RS-07C

**Required outputs**:
1. **docs/governance/LANGGRAPH_WORKFLOW.md**:
   - StateGraph design with checkpoint persistence
   - interrupt_before / interrupt_after patterns
   - Node types: Supervisor, MarketAnalyst, Coder, Reviewer, HumanApproval
   - Conditional edges for approval/rejection/rerouting
   - Durable execution with sync/async/exit modes
   - State persistence: InMemory → SQLite → Postgres progression

2. **docs/governance/HITL_APPROVAL_DESIGN.md**:
   - Human approval nodes placement
   - Approve / edit / reject actions
   - Resume after interruption
   - Timeout and escalation handling
   - Emergency kill switch integration

3. **docs/adr/ADR-0011-langgraph-hitl-workflow.md**
4. Update ledgers
5. **codex/tasks/PR-0007-langgraph-workflow/task.md**

---

## PHASE 7: Local Storage and Credential Rotation SOP (PR-0008)
**Goal**: Define local-only storage policies and credential rotation procedures.

**Inputs**: RS-08 documents, RS-08B artifact sheet

**Required outputs**:
1. **docs/governance/LOCAL_STORAGE_SOP.md**:
   - Local-only raw artifact workspace rules
   - Repo-external local workspace for: raw prompts, raw model outputs, raw runtime logs
   - Temporary quarantine workspace for: redaction work files, incident evidence
   - Retention policies: shortest practical local retention
   - Purge requirements: all local raw artifacts must be purgeable
   - GitHub promotion: redacted summary only

2. **docs/adr/ADR-0012-local-storage-credential-rotation.md**
3. Update ledgers
4. **codex/tasks/PR-0008-local-storage-sop/task.md**

---

## PHASE 8: Credential Rotation Execution SOP (PR-0009)
**Goal**: Define credential rotation execution procedures.

**Inputs**: RS-09 documents, RS-09B artifact sheet

**Required outputs**:
1. **docs/governance/CREDENTIAL_ROTATION_SOP.md**:
   - Rotation triggers: time-based, incident-based, exposure-suspected
   - Rotation procedures by credential type (API key, token, local reference)
   - Human approval requirements for each rotation type
   - Verification steps post-rotation
   - Rollback procedures

2. **docs/adr/ADR-0013-credential-rotation-execution.md**
3. Update ledgers
4. **codex/tasks/PR-0009-credential-rotation/task.md**

---

## PHASE 9: Secret Manager Selection (PR-0010)
**Goal**: Select secret manager approach and local storage implementation.

**Inputs**: RS-10 documents, RS-10 selection plan

**Required outputs**:
1. **docs/governance/SECRET_MANAGER_SELECTION.md**:
   - Candidate evaluation: OS keychain, local encrypted vault, password manager, cloud secret manager, hardware-backed storage
   - Evaluation criteria: security, recovery, purge capability, credential rotation support
   - Selected approach: OS keychain as primary, local encrypted vault as secondary
   - Rejected: cloud secret manager (provider dependency), plaintext file (never)

2. Update ledgers
3. **codex/tasks/PR-0010-secret-manager-selection/task.md**

---

## PHASE 10: Secret Manager Readiness Review (PR-0011)
**Goal**: Establish readiness gate for secret manager implementation.

**Inputs**: RS-11 documents, RS-11B artifact sheet

**Required outputs**:
1. **docs/governance/SECRET_MANAGER_READINESS.md**:
   - Readiness checklist
   - Security test plan validation
   - Pre-implementation requirements
   - Go/No-Go criteria

2. **docs/adr/ADR-0014-secret-manager-selection.md**
3. Update ledgers
4. **codex/tasks/PR-0011-readiness-review/task.md**

---

## PHASE 11: Narrow Implementation Plan (PR-0012)
**Goal**: Create the narrow implementation plan for secret manager and local storage.

**Inputs**: RS-12 documents, RS-12 narrow implementation plan

**Critical constraint**: This is PLANNING only — NO implementation.

**Required outputs**:
1. **docs/governance/SECRET_MANAGER_NARROW_PLAN.md**:
   - Narrow scope definition
   - Candidate target matrix (adopt/hold/no-go)
   - Minimal viable secret custody scope
   - Minimal local artifact storage scope
   - Owner/reviewer/approver model
   - Implementation preconditions
   - Go/No-Go/Hold rules

2. **docs/governance/SECRET_CUSTODY_BOUNDARY.md**:
   - Allowed custody targets
   - Forbidden custody (private keys, production credentials, wallet/signer)
   - Custody owner responsibilities

3. **docs/governance/LOCAL_ARTIFACT_STORAGE_BOUNDARY.md**:
   - Storage target definitions
   - Retention posture per artifact class
   - Purge requirements
   - GitHub promotion rules (redacted only)

4. **docs/governance/SECRET_MANAGER_SECURITY_TEST.md**:
   - Security test handoff requirements
   - Design rules under test
   - Expected results

5. **docs/adr/ADR-0015-secret-manager-narrow-impl.md**:
   - Status: Accepted
   - Explicit non-goals: NO implementation of secret manager, storage, encryption, purge, rotation
   - Allowed: docs-only planning, schema-only safe config, boundary definitions

6. Update ledgers
7. **codex/tasks/PR-0012-narrow-implementation-plan/task.md**

---

## PHASE 12: Minimal Implementation Task Design (PR-0013)
**Goal**: Design the minimal implementation task for secret manager.

**Inputs**: RS-13 documents, RS-13B artifact sheet

**Required outputs**:
1. **docs/governance/MINIMAL_IMPL_TASK_DESIGN.md**:
   - Task scope: safe config schema, no-secret fixtures, content/path security checks
   - Allowed files pattern
   - Forbidden files pattern
   - Rollback plan
   - Incident triggers

2. Update ledgers
3. **codex/tasks/PR-0013-minimal-impl-task-design/task.md**

---

## PHASE 13: Minimal Implementation Final Gate (PR-0014)
**Goal**: Final gate review before minimal implementation.

**Inputs**: RS-14 documents, RS-14 final gate

**Required outputs**:
1. **docs/governance/MINIMAL_IMPL_FINAL_GATE.md**:
   - Final checklist
   - Security precondition verification
   - Approval requirements
   - Go/No-Go decision record

2. Update ledgers
3. **codex/tasks/PR-0014-minimal-impl-final-gate/task.md**

---

## PHASE 14: Secret Manager Minimal Implementation (PR-0015)
**Goal**: Execute minimal safe implementation.

**Inputs**: RS-15 documents, RS-15 minimal implementation

**Critical constraint**: Schema/fixtures/checks ONLY — NO runtime implementation.

**Required outputs**:
1. **docs/governance/MINIMAL_IMPL_SCOPE.md**:
   - Included: safe config schema, no-secret fixtures, content/path security checks, manual review checklist, rollback plan, incident trigger list
   - Excluded: OS keychain adapter, local encrypted vault, secret manager runtime, credential rotation, CI changes

2. **schemas/secret-manager/safe-config.schema.json**:
   - Secret reference metadata (no value, no path)
   - Storage candidate enum (no plaintext default)
   - Custody owner field
   - Approval reference field
   - Incident blocker field
   - NO credential value field, NO local path field, NO provider operation field, NO execution approval field

3. **fixtures/security/secret-manager/**:
   - no-secret.valid.json: Valid fixture without credential values
   - forbidden-content.cases.json: Safe abstract negative cases

4. **tests/security/secret-manager-content-path-check.md**:
   - Content check specification (no executable scripts)
   - Path scanner logic specification
   - Documentation-only checks

5. **docs/adr/ADR-0017-secret-manager-minimal-impl.md**
6. Update ledgers with implementation decision
7. **codex/tasks/PR-0015-minimal-implementation/task.md**

---

## PHASE 15: OS Keychain Adapter Boundary (PR-0016)
**Goal**: Define OS keychain adapter boundary.

**Inputs**: RS-16 documents, RS-16B artifact sheet

**Required outputs**:
1. **docs/governance/OS_KEYCHAIN_BOUNDARY.md**:
   - Adapter scope and limitations
   - Allowed operations (read metadata only, no credential values)
   - Forbidden operations (secret retrieval, secret storage, key generation)
   - Error handling requirements
   - Incident triggers

2. **docs/adr/ADR-0016-os-keychain-adapter.md**
3. Update ledgers
4. **codex/tasks/PR-0016-os-keychain-boundary/task.md**

---

## PHASE 16: OS Keychain Adapter Task Design (PR-0017)
**Goal**: Design the OS keychain adapter implementation task.

**Inputs**: RS-17 documents, RS-17 task design

**Required outputs**:
1. **docs/governance/OS_KEYCHAIN_ADAPTER_TASK.md**:
   - Task scope for adapter implementation
   - Interface contract
   - Allowed files
   - Forbidden scope
   - Security requirements
   - Test specifications
   - Rollback plan

2. Update ledgers
3. **codex/tasks/PR-0017-os-keychain-adapter/task.md**

---

# SECTION 3: REFERENCE DOCUMENTATION

## 3.1 Architecture Design Integration

From the Japanese architecture design documents, integrate these technical decisions:

**Multi-Agent Framework**: LangGraph v1.0+ as primary orchestration
- Checkpointer for state persistence (PostgresSaver for production)
- interrupt_before/after for HITL
- Durable execution modes: sync/async/exit

**Local LLM Stack**: Ollama on port 11434
- Primary: Llama 3.1 8B Instruct Q4_K_M (~5GB, 30-45 t/s)
- Secondary: Qwen2.5 7B Q5_K_M, Phi-4 14B Q4_K_M
- Guardrail: Llama Guard 3 8B (CPU offload)
- VRAM budget: RTX 4070 Ti 12GB → effective ~10.8GB

**Cloud Escalation**: LiteLLM Proxy as unified exit
- Budget limits: provider_budget_config + key budgets + tag budgets
- Models: Claude Sonnet 4.5, GPT-5, Gemini 2.5 Pro (escalation only)

**MCP Implementation**: FastMCP (Python)
- Transport: stdio for local tools, Streamable HTTP for remote
- Auth: OAuth 2.1 + Resource Indicator for production MCP servers
- Version: 2025-11-25 spec (URL Mode Elicitation, Sampling with Tools)

**Agent Roles (5-role configuration)**:
1. Orchestrator Agent: LangGraph StateGraph supervisor
2. Market Analyst Agent: trend analysis, competitive research (cloud model)
3. Coder Agent: code generation, script writing (cloud/local hybrid)
4. Reviewer Agent: code review, security check (local model)
5. Execution MCP: sandboxed code execution (isolated)

**Harness Engineering**:
- Max steps limit: 15 steps per workflow
- Token budget: 50,000 tokens or $1.00 per session
- Circuit breaker: hash comparison for loop detection (last 3 turns)
- Sandbox: Firecracker microVM for code execution
- Audit: JSONL decision provenance logs with trace_id, actor, event, reasoning_trace, governance_policy

## 3.2 Evidence Ledger Reference

All decisions must be traceable to:
- LangGraph durable execution documentation (checkpoints, interrupts)
- MCP specification (host-client-server separation, authorization)
- OpenAI Codex documentation (isolated task execution)
- GitHub Docs (protected branches, CODEOWNERS, issue forms)
- Base Docs (public endpoint limitations, Flashblocks)
- FastMCP documentation (tool registration, auth middleware)
- LiteLLM documentation (budget controls, routing)

---

# SECTION 4: EXECUTION RULES

## 4.1 Order of Execution
1. Execute phases in numerical order (0 through 16)
2. Each phase's outputs become inputs for subsequent phases
3. Ledger updates happen after each phase
4. ADR creation follows artifact creation for each phase

## 4.2 File Permissions
- **ALLOWED**: docs/**, research/**, labs/**/README.md, codex/**, .github/**, schemas/**, fixtures/**, tests/**, README.md, SAFETY.md
- **FORBIDDEN**: .env, .env.*, runtime/**, src/** (unless explicitly scoped), apps/**, packages/** (except .gitkeep), package.json, requirements.txt, docker-compose.yml, any wallet/signer/deploy/execution file

## 4.3 Content Constraints
- NO credential values in any file
- NO local secret paths in any file
- NO real-looking secret examples in fixtures (use abstract labels only)
- NO executable code in docs/ or research/
- NO CI changes without explicit approval
- NO package installations
- NO provider-specific implementation details
- NO runtime code generation

## 4.4 Quality Standards
- Every governance doc must have required headings
- Every ADR must have: Status, Context, Decision, Rejected Alternatives, Consequences, Risks, Follow-ups
- Every task.md must have: task_id, title, status, human_approval_required, task_class, risk_level, goal, background, inputs, in_scope, out_of_scope, allowed_files, forbidden_files, required_outputs, prohibited_work, implementation_notes, tests_or_checks, acceptance_criteria, review_checklist, rollback_plan
- Cross-references between documents must be explicit
- All ledger entries must use the defined schemas

## 4.5 Stopping Conditions
STOP immediately if any of the following occur:
- Secret values appear in any file
- Local paths appear in any file
- Runtime code is requested
- CI/GitHub Actions modification is requested
- Wallet/signer/deploy/approve/swap/transfer code is requested
- Provider integration is requested
- Scope expansion beyond approved boundaries
- approval semantics drift toward execution approval

---

# SECTION 5: REVIEW AND ACCEPTANCE

## 5.1 Self-Review Checklist (apply before completing)
- [ ] All 17 phases have required outputs
- [ ] All ADRs have required sections
- [ ] All ledger schemas are complete
- [ ] Cross-references between documents exist
- [ ] No credential values in any file
- [ ] No local paths in any file
- [ ] No executable code in docs/ or research/
- [ ] No forbidden files edited
- [ ] Product boundary statements are explicit
- [ ] Hard bans are documented in SAFETY.md
- [ ] All task.md files are self-contained

## 5.2 Human Review Required Before
- Any merge to main branch
- Any scope expansion
- Any ADR status change to "Accepted"
- Any modification to hard bans
- Any ledger entry with severity High or above

---

# END OF MASTER PROMPT
