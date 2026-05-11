# AIDEN Research OS - Complete Directory Structure
# For OpenAI Codex App Batch Execution
# Generated from RS-00 through RS-17 + Architecture Design Documents

aiden-research-os/                          # Personal AI Research OS root
│
├── README.md                               # Project overview and entry point
├── SAFETY.md                               # Safety constraints and hard bans
├── .gitignore                              # Git ignore patterns (no secrets, no runtime logs)
│
├── .codex/                                 # Codex App configuration and prompts
│   ├── instructions.md                     # Master system instructions for Codex
│   ├── review.md                           # Review criteria and acceptance standards
│   └── tasks/                              # Individual task definitions
│       ├── PR-0001-root-scaffold.md
│       ├── PR-0002-cloud-local-role-split.md
│       ├── PR-0003-governance-ledger.md
│       ├── PR-0004-runtime-boundary.md
│       ├── PR-0005-security-test-plan.md
│       ├── PR-0006-mcp-boundary.md
│       ├── PR-0007-langgraph-workflow.md
│       ├── PR-0008-local-storage-sop.md
│       ├── PR-0009-credential-rotation.md
│       ├── PR-0010-secret-manager-selection.md
│       ├── PR-0011-readiness-review.md
│       ├── PR-0012-narrow-implementation-plan.md
│       ├── PR-0013-minimal-impl-task-design.md
│       ├── PR-0014-minimal-impl-final-gate.md
│       ├── PR-0015-minimal-implementation.md
│       ├── PR-0016-os-keychain-boundary.md
│       └── PR-0017-os-keychain-adapter.md
│
├── .github/                                # GitHub governance surface
│   ├── CODEOWNERS                          # Code ownership rules
│   ├── PULL_REQUEST_TEMPLATE.md            # PR template with governance checklist
│   ├── cla-bot-config.yml                  # CLA bot configuration
│   ├── CLA.md                              # Contributor License Agreement
│   ├── CONTRIBUTING.md                     # Contribution guidelines
│   ├── FUNDING.yml                         # Funding/sponsorship info
│   ├── labeler.yml                         # Auto-labeler config
│   ├── CODE_OF_CONDUCT.md                  # Community standards
│   ├── ISSUE_TEMPLATE/                     # Issue form templates
│   │   ├── research_sprint.yml             # Research sprint intake form
│   │   ├── codex_task.yml                  # Codex task request form
│   │   ├── bug_report.yml                  # Bug report form
│   │   ├── bug_report.md                   # Bug report markdown fallback
│   │   ├── feature_request.yml             # Feature request form
│   │   ├── feature_request.md              # Feature request markdown fallback
│   │   ├── skill_request.md                # Skill request form
│   │   └── skill_submission.yml            # Skill submission form
│   └── workflows/                          # GitHub Actions workflows
│       ├── governance-ci.yml               # Governance artifact validation CI
│       └── pr-labeler.yml                  # PR auto-labeling
│
├── docs/                                   # Documentation and governance
│   ├── system/                             # System-level documentation
│   │   ├── PRODUCT_BOUNDARY.md             # Product identity and boundaries (RS-00)
│   │   ├── SYSTEM_OF_SYSTEMS.md            # Component architecture (RS-00)
│   │   ├── EXECUTION_BOUNDARY.md           # Execution separation rules (RS-04)
│   │   ├── ARCHITECTURE.md                 # Technical architecture overview
│   │   └── TECH_STACK_MATRIX.md            # Tech stack selection matrix
│   │
│   ├── governance/                         # Governance policies and procedures
│   │   ├── SOURCE_OF_TRUTH.md              # GitHub SoT policy (RS-01)
│   │   ├── REPOSITORY_TOPOLOGY.md          # Repo structure decisions (RS-01)
│   │   ├── ARTIFACT_TAXONOMY.md            # Artifact classification (RS-01)
│   │   ├── DEEP_RESEARCH_FLOW.md           # Research workflow specification
│   │   ├── APPROVAL_FLOW.md                # Human approval process
│   │   ├── RUNBOOK.md                      # Operational runbook
│   │   ├── CLOUD_LOCAL_SPLIT.md            # Cloud AI x Local AI role split (RS-02)
│   │   ├── LEDGER_SCHEMA.md                # Governance ledger schema (RS-03)
│   │   ├── REDACTION_WORKFLOW.md           # Data redaction procedures (RS-03)
│   │   ├── MCP_BOUNDARY.md                 # MCP tool permission model (RS-06)
│   │   ├── MCP_TOOL_PERMISSION_MODEL.md    # MCP authorization matrix (RS-06)
│   │   ├── HITL_APPROVAL_DESIGN.md         # Human-in-the-loop design (RS-07)
│   │   ├── LANGGRAPH_WORKFLOW.md           # LangGraph workflow spec (RS-07)
│   │   ├── LOCAL_STORAGE_SOP.md            # Local storage SOP (RS-08)
│   │   ├── CREDENTIAL_ROTATION_SOP.md      # Credential rotation SOP (RS-09)
│   │   ├── SECRET_MANAGER_SELECTION.md     # Secret manager selection (RS-10)
│   │   ├── SECRET_MANAGER_READINESS.md     # Readiness review checklist (RS-11)
│   │   ├── SECRET_MANAGER_NARROW_PLAN.md   # Narrow implementation plan (RS-12)
│   │   ├── SECRET_CUSTODY_BOUNDARY.md      # Secret custody boundary (RS-12)
│   │   ├── LOCAL_ARTIFACT_STORAGE_BOUNDARY.md  # Local artifact storage rules (RS-12)
│   │   ├── SECRET_MANAGER_SECURITY_TEST.md # Security test handoff (RS-12)
│   │   ├── MINIMAL_IMPL_TASK_DESIGN.md     # Minimal impl task design (RS-13)
│   │   ├── MINIMAL_IMPL_FINAL_GATE.md      # Final gate checklist (RS-14)
│   │   ├── MINIMAL_IMPL_SCOPE.md           # Minimal implementation scope (RS-15)
│   │   ├── OS_KEYCHAIN_BOUNDARY.md         # OS keychain adapter boundary (RS-16)
│   │   └── OS_KEYCHAIN_ADAPTER_TASK.md     # OS keychain adapter task (RS-17)
│   │
│   ├── adr/                                # Architecture Decision Records
│   │   ├── ADR-0001-product-is-aiden-research-os.md      # Product identity ADR (RS-00)
│   │   ├── ADR-0002-github-is-source-of-truth.md         # GitHub SoT ADR (RS-01)
│   │   ├── ADR-0003-initial-monorepo-topology.md         # Monorepo decision (RS-01)
│   │   ├── ADR-0004-market-labs-directory-is-labs.md     # labs/ directory ADR (RS-01)
│   │   ├── ADR-0005-cloud-local-role-split.md            # Cloud/Local split ADR (RS-02)
│   │   ├── ADR-0006-governance-ledger-schema.md          # Ledger schema ADR (RS-03)
│   │   ├── ADR-0007-runtime-integration-boundary.md      # Runtime boundary ADR (RS-04)
│   │   ├── ADR-0008-aiden-runtime-boundary.md            # AIDEN runtime ADR (RS-04)
│   │   ├── ADR-0009-research-lab-security-test-plan.md   # Security test ADR (RS-05)
│   │   ├── ADR-0010-mcp-boundary-tool-permission.md      # MCP boundary ADR (RS-06)
│   │   ├── ADR-0011-langgraph-hitl-workflow.md           # LangGraph HITL ADR (RS-07)
│   │   ├── ADR-0012-local-storage-credential-rotation.md # Storage/rotation ADR (RS-08)
│   │   ├── ADR-0013-credential-rotation-execution.md     # Rotation execution ADR (RS-09)
│   │   ├── ADR-0014-secret-manager-selection.md          # Secret manager ADR (RS-10)
│   │   ├── ADR-0015-secret-manager-narrow-impl.md        # Narrow impl ADR (RS-12)
│   │   ├── ADR-0016-os-keychain-adapter.md               # OS keychain ADR (RS-16)
│   │   └── ADR-0017-secret-manager-minimal-impl.md       # Minimal impl ADR (RS-15)
│   │
│   ├── security/                           # Security documentation
│   │   ├── HARDENING_POSTURE.md            # Security hardening posture
│   │   ├── THREAT_MODEL.md                 # Research lab threat model
│   │   ├── SECURITY_LEDGER.md              # Security decision ledger
│   │   ├── HUMAN_APPROVAL_KILL_SWITCH.md   # Human approval kill switch
│   │   ├── PRODUCTION_EXECUTION_PROHIBITION.md  # Production execution ban
│   │   ├── MODEL_ROUTING_COST_LIMITS.md    # Model routing budget limits
│   │   ├── NETWORK_RPC_ALLOWLIST.md        # Network RPC allowlist
│   │   ├── SIMULATION_EVIDENCE_FORMAT.md   # Simulation evidence schema
│   │   └── AUDIT_LEDGER.md                 # Audit trail ledger
│   │
│   ├── reference/                          # Reference documentation
│   │   ├── AIDEN_CAPABILITIES_GUIDE.md     # AIDEN capabilities guide
│   │   ├── PERSONAL_AI_COMPANY_DESIGN.md   # Personal AI company design
│   │   ├── ARCHITECTURE_DESIGN_JA.md       # Japanese architecture design
│   │   ├── DEEP_RESEARCH_REPORT_JA.md      # Japanese deep research report
│   │   ├── OSS_CATALOG_L2.md               # Base L2 OSS catalog
│   │   ├── OSS_CATALOG_BASE.md             # Base OSS catalog
│   │   └── AI_AUTONOMOUS_RESEARCH_LAB.md   # AI autonomous research lab report
│   │
│   └── templates/                          # Document templates
│       ├── sprint-report-template.md
│       ├── risk-assessment-template.md
│       └── incident-report-template.md
│
├── research/                               # Research outputs and ledgers
│   ├── sprints/                            # Research sprint reports
│   │   ├── README.md
│   │   ├── RS-00-product-boundary.md
│   │   ├── RS-01-github-sot-topology.md
│   │   ├── RS-02-cloud-local-split.md
│   │   ├── RS-03-governance-ledger.md
│   │   ├── RS-04-runtime-boundary.md
│   │   ├── RS-05-security-test-plan.md
│   │   ├── RS-06-mcp-boundary.md
│   │   ├── RS-07-langgraph-workflow.md
│   │   ├── RS-08-local-storage-sop.md
│   │   ├── RS-09-credential-rotation.md
│   │   ├── RS-10-secret-manager-selection.md
│   │   ├── RS-11-readiness-review.md
│   │   ├── RS-12-narrow-implementation-plan.md
│   │   ├── RS-13-minimal-impl-task-design.md
│   │   ├── RS-14-minimal-impl-final-gate.md
│   │   ├── RS-15-minimal-implementation.md
│   │   ├── RS-16-os-keychain-boundary.md
│   │   └── RS-17-os-keychain-adapter.md
│   │
│   ├── ledgers/                            # Governance ledgers
│   │   ├── research-ledger.md              # Research activity log
│   │   ├── evidence-ledger.md              # Evidence and findings log
│   │   ├── risk-ledger.md                  # Risk tracking (RS-03)
│   │   ├── decision-log.md                 # Decision history (RS-03)
│   │   ├── approval-record.md              # Human approval canonical record (RS-03)
│   │   ├── redaction-checklist.md          # Redaction audit trail (RS-03)
│   │   ├── incident-record.md             # Security incidents (RS-03)
│   │   ├── task-promotion-record.md        # Task promotion history (RS-03)
│   │   ├── open-questions.md              # Open questions backlog (RS-03)
│   │   └── phase-gates/                   # Phase gate records
│   │       ├── README.md
│   │       └── PG-0001-through-PG-0017.md  # All phase gate decisions
│   │
│   ├── findings/                           # Research findings
│   │   ├── README.md
│   │   ├── framework-comparison.md         # Multi-agent framework comparison
│   │   ├── local-llm-evaluation.md         # Local LLM evaluation results
│   │   ├── mcp-spec-analysis.md            # MCP specification analysis
│   │   ├── cost-optimization-study.md      # Cost optimization study
│   │   └── security-assessment.md          # Security posture assessment
│   │
│   └── backlog.md                          # Research backlog and queued items
│
├── labs/                                   # Market research labs
│   ├── base-dex-lab/                       # Base DEX Lab (one-of-many)
│   │   ├── README.md
│   │   ├── ARCHITECTURE.md
│   │   ├── EVIDENCE_SCHEMA.md
│   │   ├── RISK_FRAMEWORK.md
│   │   └── PROMOTION_RULES.md
│   │
│   ├── prediction-market-lab/              # Prediction Market Lab
│   │   ├── README.md
│   │   ├── ARCHITECTURE.md
│   │   ├── EVIDENCE_SCHEMA.md
│   │   ├── SHADOW_MODE_POLICY.md
│   │   └── PROMOTION_RULES.md
│   │
│   └── perp-dex-lab/                       # Perp DEX Lab
│       ├── README.md
│       ├── ARCHITECTURE.md
│       ├── EVIDENCE_SCHEMA.md
│       ├── PAPER_TRADING_POLICY.md
│       └── PROMOTION_RULES.md
│
├── packages/                               # Reserved for future package split
│   └── .gitkeep
│
├── schemas/                                # JSON schemas and validation
│   ├── governance/                         # Governance schemas
│   │   ├── approval-record.schema.json
│   │   ├── risk-ledger.schema.json
│   │   ├── decision-log.schema.json
│   │   └── incident-record.schema.json
│   ├── research-lab/                       # Research lab schemas
│   │   ├── audit-event.schema.json
│   │   ├── simulation-result.schema.json
│   │   └── evidence-bundle.schema.json
│   └── secret-manager/                     # Secret manager schemas
│       ├── safe-config.schema.json
│       └── reference-metadata.schema.json
│
├── fixtures/                               # Test fixtures and sample data
│   ├── governance/                         # Governance fixtures
│   │   ├── safe-approval-fixtures.json
│   │   └── unsafe-approval-fixtures.json
│   ├── security/                           # Security test fixtures
│   │   ├── secret-manager/
│   │   │   ├── no-secret.valid.json
│   │   │   └── forbidden-content.cases.json
│   │   └── audit-events/
│   │       ├── execution-approved.json
│   │       └── execution-denied.json
│   └── research-lab/                       # Research lab fixtures
│       ├── safe/
│       └── unsafe/
│
├── tests/                                  # Test specifications
│   ├── security/                           # Security tests
│   │   ├── secret-manager-content-path-check.md
│   │   ├── forbidden-content-scan.md
│   │   └── approval-semantic-check.md
│   └── governance/                         # Governance validation tests
│       ├── artifact-existence-check.md
│       └── schema-validation-check.md
│
├── codex/                                  # Codex task artifacts
│   ├── templates/                          # Reusable task templates
│   │   ├── task-template.md                # Standard task template
│   │   └── pr-audit-template.md            # PR audit checklist template
│   └── tasks/                              # Executable task definitions
│       ├── PR-0001-root-scaffold/
│       │   └── task.md
│       ├── PR-0002-cloud-local-role-split/
│       │   └── task.md
│       ├── PR-0003-governance-ledger/
│       │   └── task.md
│       ├── PR-0004-runtime-boundary/
│       │   └── task.md
│       ├── PR-0005-security-test-plan/
│       │   └── task.md
│       ├── PR-0006-mcp-boundary/
│       │   └── task.md
│       ├── PR-0007-langgraph-workflow/
│       │   └── task.md
│       ├── PR-0008-local-storage-sop/
│       │   └── task.md
│       ├── PR-0009-credential-rotation/
│       │   └── task.md
│       ├── PR-0010-secret-manager-selection/
│       │   └── task.md
│       ├── PR-0011-readiness-review/
│       │   └── task.md
│       ├── PR-0012-narrow-implementation-plan/
│       │   └── task.md
│       ├── PR-0013-minimal-impl-task-design/
│       │   └── task.md
│       ├── PR-0014-minimal-impl-final-gate/
│       │   └── task.md
│       ├── PR-0015-minimal-implementation/
│       │   └── task.md
│       ├── PR-0016-os-keychain-boundary/
│       │   └── task.md
│       └── PR-0017-os-keychain-adapter/
│           └── task.md
│
├── scripts/                                # Utility scripts (read-only)
│   ├── validate-governance.sh              # Governance artifact validator
│   └── generate-ledger-report.sh           # Ledger report generator
│
├── assets/                                 # Static assets
│   ├── images/
│   └── diagrams/
│
├── landing/                                # Landing page assets
│
├── skills/                                 # Skill definitions
│   ├── learned/
│   │   ├── approved/
│   │   └── pending/
│   └── requests/
│
└── config/                                 # Configuration files
    └── banned-topics.json                  # Banned topic list

# ============================================================
# DIRECTORY RESPONSIBILITY MATRIX
# ============================================================
# path                          owner                   reviewer                human_approval  allowed_content                     forbidden_content
# /                             Human repo owner        Human final approver    true            README, SAFETY, policy links        runtime code, secrets, deploy logic
# docs/system/                  Product steward         Human final approver    true            boundary/system markdown            code, secrets, runtime config
# docs/governance/              Governance steward      Human final approver    true            governance markdown                 external write design, secret-handling logic
# docs/adr/                     Decision author         Human final approver    true            ADR drafts and accepted ADRs        code, env values, runtime execution details
# docs/security/                Security steward        Human final approver    true            security policy markdown            vulnerability disclosure, secret paths
# research/sprints/             Research author         Governance reviewer     false           sprint reports, README              deploy specs, runtime code, API keys
# research/ledgers/             Research steward        Governance reviewer     false           markdown ledgers, schemas           secrets, executable code, live integration settings
# research/phase-gates/         Governance steward      Human final approver    true            phase gate records                  auto-approval logic, runtime authority
# labs/*/                       Lab steward             Governance reviewer     false           README and specs only               live API code, wallet/signing, execution logic
# packages/                     Package steward         Human final approver    true            .gitkeep only in PR-0001            package manifests, runtime code
# codex/templates/              Governance steward      Human final approver    true            task/pr-audit templates             codegen logic, runtime scripts
# codex/tasks/                  Task author             Human final approver    true            task definitions, inputs            secrets, env values, executable code
# schemas/                      Schema steward          Governance reviewer     true            JSON schemas                        secret values, local paths
# fixtures/                     Fixture steward         Governance reviewer     true            safe abstract fixtures              real-looking secrets, local paths
# tests/                        Test steward            Governance reviewer     true            test specifications                 executable test scripts (CI only)
# .github/                      Governance steward      Human final approver    true            CODEOWNERS, templates, workflows    secret-dependent automation
# .codex/                       System architect        Human final approver    true            instructions, tasks, review criteria executable code, secrets
