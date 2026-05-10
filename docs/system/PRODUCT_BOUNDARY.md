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
