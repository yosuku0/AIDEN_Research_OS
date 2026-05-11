# Prediction Market Lab

## Purpose

The Prediction Market Lab is a research scaffold for analyzing prediction market protocols, oracle resolution systems, and market efficiency mechanisms. This lab examines how decentralized markets aggregate information and resolve outcomes through documentation-only research.

This lab does not create markets, place bets, or manage positions. All outputs are governance artifacts for review.

## Boundary

Research/control-plane artifact only. No market creation, position taking, oracle manipulation, or production-write access.

Research outputs follow the AIDEN governance pipeline:
1. Artifact creation
2. Redaction check (no credentials, no execution paths)
3. HumanApproval gate review
4. Ledger update with cross-references

## Research Questions

1. How do different oracle systems (centralized, decentralized, hybrid) affect resolution accuracy and timeliness?
2. What market mechanisms (CFMM, orderbook, parimutuel) achieve highest price discovery efficiency?
3. How do resolution delays impact trader participation and market liquidity?
4. What is the relationship between market liquidity and prediction accuracy (weighted by stake)?
5. How can manipulation-resistant market design be evaluated through simulation?

## Methodology

### Data Collection
- Abstract market outcome datasets (no real market data)
- Oracle behavior simulation under different conditions
- Mechanism comparison using standardized efficiency metrics
- Participation pattern analysis with simulated agents

### Analysis Approach
1. **Oracle Comparison**: Accuracy, latency, and cost analysis across oracle types
2. **Mechanism Efficiency**: Price discovery quality for CFMM vs orderbook vs parimutuel
3. **Delay Impact Study**: Liquidity and participation metrics at various resolution delays
4. **Liquidity-Accuracy Correlation**: Stake-weighted accuracy vs market depth
5. **Manipulation Resistance**: Attack vector simulation and mitigation effectiveness

### Tools Used
- `schemas/research-lab/simulation-result.schema.json` for simulation outcomes
- `schemas/research-lab/evidence-bundle.schema.json` for compiled evidence
- `schemas/research-lab/audit-event.schema.json` for research tracking

## Schema Reference

| Schema | Purpose |
|--------|---------|
| `schemas/research-lab/simulation-result.schema.json` | Oracle, mechanism, efficiency simulations |
| `schemas/research-lab/evidence-bundle.schema.json` | Evidence compilation |
| `schemas/research-lab/audit-event.schema.json` | Activity audit trail |
| `schemas/governance/decision-log.schema.json` | Methodology decisions |

## Evidence Structure

```
labs/prediction-market-lab/
  README.md              # This file
  evidence/
    oracle-comparison.md      # Oracle accuracy/latency analysis
    mechanism-efficiency.md   # Price discovery comparison
    delay-impact.md           # Resolution delay effects
    liquidity-accuracy.md     # Depth vs accuracy correlation
    manipulation-resistance.md # Attack vector simulation
```

Evidence requirements:
- Abstract market identifiers (no real market references)
- No outcome values that could be construed as predictions
- Methodology documentation without implementation
- Audit event linkage (AE-XXXX)

## References

- **ADR-0004**: Market labs directory (`labs/`)
- **PRODUCT_BOUNDARY.md**: Research-only scope
- **THREAT_MODEL.md**: Oracle risk factors
- **SAFETY.md**: Hard-ban rules
- **APPROVAL_FLOW.md**: Review and approval process
