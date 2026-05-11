# Perp DEX Lab

## Purpose

The Perp DEX Lab is a research scaffold for analyzing perpetual decentralized exchange protocols. This lab focuses on funding rate mechanisms, liquidation patterns, leverage structures, and risk management systems through documentation-only research artifacts.

This lab does not implement trading strategies, execute trades, or manage positions. All outputs are governance artifacts subject to HumanApproval review.

## Boundary

Research/control-plane artifact only. No execution authority, signing capability, position management, or production-write access.

Research outputs flow through the AIDEN governance pipeline:
1. Artifact creation by Codex
2. Redaction verification (no secrets, no executable code)
3. HumanApproval gate review with 8-item checklist
4. Ledger update with approval_criteria_met documentation

## Research Questions

1. How do funding rates correlate with underlying asset volatility across protocols?
2. What liquidation patterns emerge under different leverage multipliers (2x, 5x, 10x, 20x)?
3. How do perpetual DEX mechanisms (vAMM, orderbook, hybrid) differ in capital efficiency?
4. What is the risk profile of leveraged positions during high-volatility events?
5. How do insurance fund mechanisms compare across perpetual protocols?

## Methodology

### Data Collection
- Simulated funding rate histories (abstracted, no real protocol data)
- Liquidation scenario modeling with controlled variables
- Protocol mechanism comparison using standardized metrics
- Risk metric calculation using documented formulas

### Analysis Approach
1. **Funding Rate Correlation**: Volatility index vs funding rate regression
2. **Liquidation Scenario Modeling**: Position health factor simulation at various leverage levels
3. **Mechanism Comparison**: vAMM vs orderbook vs hybrid capital efficiency analysis
4. **Risk Profile Assessment**: Value-at-Risk simulation for leveraged positions
5. **Insurance Fund Analysis**: Capacity vs historical drawdown comparison

### Tools Used
- `schemas/research-lab/simulation-result.schema.json` for structured outcomes
- `schemas/research-lab/evidence-bundle.schema.json` for evidence compilation
- `schemas/research-lab/audit-event.schema.json` for activity tracking
- `schemas/governance/risk-ledger.schema.json` for risk documentation

## Schema Reference

| Schema | Purpose |
|--------|---------|
| `schemas/research-lab/simulation-result.schema.json` | Funding rate, liquidation, risk simulations |
| `schemas/research-lab/evidence-bundle.schema.json` | Compiled research evidence |
| `schemas/research-lab/audit-event.schema.json` | Research activity tracking |
| `schemas/governance/risk-ledger.schema.json` | Risk identification and mitigation |
| `schemas/governance/decision-log.schema.json` | Methodology decisions |

## Evidence Structure

```
labs/perp-dex-lab/
  README.md              # This file
  evidence/
    funding-correlation.md    # Funding rate vs volatility findings
    liquidation-scenarios.md  # Leverage liquidation modeling
    mechanism-comparison.md   # vAMM vs orderbook analysis
    risk-profiles.md          # VaR simulation results
    insurance-funds.md        # Protocol insurance comparison
```

Evidence requirements:
- Abstract protocol identifiers (no real protocol names in fixtures)
- No position sizes or account references
- Formula documentation without implementation code
- All evidence linked to audit events (AE-XXXX)

## References

- **ADR-0004**: Market labs directory (`labs/`)
- **EXECUTION_BOUNDARY.md**: Research/execution separation
- **THREAT_MODEL.md**: Perp-specific risk factors
- **SAFETY.md**: Hard-ban rules
- **APPROVAL_FLOW.md**: Review process
