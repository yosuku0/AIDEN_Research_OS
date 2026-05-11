---
task_id: PR-0001
title: Root scaffold for AIDEN Research OS
status: ready
human_approval_required: true
task_class: scaffold-only
risk_level: medium
---

# Goal
Create the repository scaffold and minimum governance documents for AIDEN Research OS.

# Background
This repository is a research/control-plane scaffold and not a trading implementation.

# Inputs
- Product umbrella: Personal AI Research OS
- Operational name: AIDEN Research OS
- GitHub is Source of Truth
- Human is final approver
- AIDEN does not sign, deploy, approve, swap, or perform production write
- Base DEX Lab is one market domain among several labs

# In Scope
- Create docs directories and PRODUCT_BOUNDARY.md, SYSTEM_OF_SYSTEMS.md
- Create ADR-0001 through ADR-0004
- Create governance docs: SOURCE_OF_TRUTH.md, REPOSITORY_TOPOLOGY.md, ARTIFACT_TAXONOMY.md, APPROVAL_FLOW.md, DEEP_RESEARCH_FLOW.md, RUNBOOK.md
- Create research/ledgers/ with all ledger files (empty schemas)
- Create labs/**/README.md placeholders
- Create .github/CODEOWNERS, PULL_REQUEST_TEMPLATE.md, ISSUE_TEMPLATE/*.md, workflows/governance-ci.yml
- Create codex/templates/task-template.md, pr-audit-template.md
- Create this task file

# Out of Scope
- Wallet client, private key handling, transaction signing
- Deploy scripts, approve/swap/bridge/transfer
- Market-specific bot logic, runtime code
- Provider SDK integration, package install
- External write integrations

# Allowed Files
- README.md, SAFETY.md
- docs/system/*.md
- docs/governance/*.md
- docs/adr/ADR-0001*.md, ADR-0002*.md, ADR-0003*.md, ADR-0004*.md
- research/**/README.md, research/ledgers/*.md
- labs/**/README.md
- codex/templates/*.md, codex/tasks/PR-0001*/task.md
- .github/CODEOWNERS, .github/PULL_REQUEST_TEMPLATE.md
- .github/ISSUE_TEMPLATE/*.md, .github/workflows/*.yml
- packages/.gitkeep

# Forbidden Files
- .env, .env.*
- package.json, requirements.txt
- runtime/**, src/**
- Any wallet/signer/deploy/execution file

# Required Outputs
1. README.md with product identity and architecture overview
2. SAFETY.md with hard bans
3. docs/system/PRODUCT_BOUNDARY.md
4. docs/system/SYSTEM_OF_SYSTEMS.md
5. docs/adr/ADR-0001-product-is-aiden-research-os.md
6. docs/adr/ADR-0002-github-is-source-of-truth.md
7. docs/adr/ADR-0003-initial-monorepo-topology.md
8. docs/adr/ADR-0004-market-labs-directory-is-labs.md
9. docs/governance/SOURCE_OF_TRUTH.md
10. docs/governance/REPOSITORY_TOPOLOGY.md
11. docs/governance/ARTIFACT_TAXONOMY.md
12. docs/governance/APPROVAL_FLOW.md
13. docs/governance/DEEP_RESEARCH_FLOW.md
14. docs/governance/RUNBOOK.md
15. research/ledgers/*.md (8 files)
16. labs/base-dex-lab/README.md
17. labs/prediction-market-lab/README.md
18. labs/perp-dex-lab/README.md
19. .github/CODEOWNERS
20. .github/PULL_REQUEST_TEMPLATE.md
21. .github/ISSUE_TEMPLATE/*.yml (research_sprint, codex_task, bug_report, feature_request)
22. .github/workflows/governance-ci.yml
23. codex/templates/task-template.md
24. codex/templates/pr-audit-template.md
25. codex/tasks/PR-0001-root-scaffold/task.md

# Prohibited Work
- Do not request secrets
- Do not add provider SDKs
- Do not add runtime code
- Do not add deploy/approve/swap paths
- Do not add package installs
- Do not create files outside allowed_files

# Acceptance Criteria
- All 25 required files exist
- Boundary statements are explicit in every file
- GitHub SoT is explicit
- Human final approval is explicit
- No execution authority is introduced
- Hard bans are documented
- Cross-references between documents exist

# Rollback Plan
Revert the PR entirely if forbidden scope is touched or required outputs are incomplete.

# Related Research
- RS-00 System Boundary / Product Definition

# Related ADR
- ADR-0001-product-is-aiden-research-os
