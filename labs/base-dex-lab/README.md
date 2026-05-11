# Base DEX Lab

## Purpose

The Base DEX Lab is a research scaffold for analyzing decentralized exchange protocols operating on the Base L2 chain. This lab focuses on understanding liquidity distribution, swap routing mechanics, fee structures, and trading patterns through documentation-only research artifacts.

This lab does not implement, deploy, or interact with any live protocols. All outputs are governance artifacts: documentation, schemas, fixtures, and evidence bundles.

## Boundary

This is a research/control-plane artifact only. It grants no signing authority, deployment capability, capital allocation, swap execution, bridge operation, or production-write access.

All research outputs must pass through the standard AIDEN governance pipeline:
1. Artifact creation by Codex
2. Redaction check (no secrets, no execution authority)
3. HumanApproval gate review
4. Ledger update and evidence linking

## Research Questions

1. How is liquidity distributed across Base DEX pools, and what concentration patterns emerge?
2. What swap routing patterns are most common for different trade sizes?
3. How do fee tiers (0.01%, 0.05%, 0.3%, 1%) correlate with trading volume and LP returns?
4. What is the relationship between TVL (Total Value Locked) and trading efficiency metrics?
5. How do concentrated liquidity positions affect price impact for retail vs institutional-sized trades?

## Methodology

### Data Collection
- Simulated on-chain data based on public DEX analytics
- Aggregated metrics (no individual transaction traces)
- Abstracted pool identifiers (no contract addresses)

### Analysis Approach
1. **Liquidity Distribution Analysis**: Pool depth comparison across fee tiers
2. **Routing Pattern Study**: Common path analysis for token pairs
3. **Fee Structure Correlation**: Volume-fee tier regression
4. **TVL-Efficiency Modeling**: Relationship between locked capital and execution quality
5. **Concentrated Liquidity Impact**: Position width vs price impact simulation

### Tools Used
- `schemas/research-lab/simulation-result.schema.json` for structured results
- `schemas/research-lab/evidence-bundle.schema.json` for evidence compilation
- `schemas/research-lab/audit-event.schema.json` for research activity tracking

## Schema Reference

This lab uses the following schemas:

| Schema | Purpose |
|--------|---------|
| `schemas/research-lab/simulation-result.schema.json` | Store simulation outcomes (liquidity, routing, fee analysis) |
| `schemas/research-lab/evidence-bundle.schema.json` | Compile evidence from multiple sources |
| `schemas/research-lab/audit-event.schema.json` | Track research activities for audit trail |
| `schemas/governance/decision-log.schema.json` | Record methodology decisions |

## Evidence Structure

Evidence is stored as documentation-only artifacts:

```
labs/base-dex-lab/
  README.md              # This file
  evidence/
    liquidity-analysis.md     # Pool depth findings
    routing-patterns.md       # Common swap paths
    fee-correlation.md        # Fee-tier volume analysis
    tvl-efficiency.md         # Capital efficiency metrics
    concentrated-liquidity.md # Position impact study
  fixtures/
    # Reference fixtures/security/secret-manager/ for data format examples
```

All evidence files must:
- Use abstract identifiers (no real contract addresses)
- Contain no credential values or local paths
- Pass redaction checklist (RC-XXXX)
- Be linked to audit events (AE-XXXX)

## References

- **ADR-0004**: Market labs directory structure (`labs/` is the canonical location)
- **PRODUCT_BOUNDARY.md**: Research-only scope definition
- **EXECUTION_BOUNDARY.md**: Research/execution separation
- **SAFETY.md**: Hard-ban rules (no deployment, no signing)
- **APPROVAL_FLOW.md**: Artifact review and approval process
- **ADR_DIFFERENTIATION_GUIDE.md**: ADR risk differentiation standards
