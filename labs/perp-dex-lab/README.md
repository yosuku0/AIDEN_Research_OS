# Perp DEX Lab

## Purpose

Research lab for analyzing perpetual DEX (Perpetual Decentralized Exchange) protocols, funding rate mechanisms, liquidation patterns, and leverage trading structures. Documentation-only research artifact.

## Boundary

Research scaffold only. No execution, signing, capital deployment, or production-write authority. All outputs are governance artifacts.

## Research Questions

1. How do funding rates correlate with market volatility?
2. What liquidation patterns emerge under high leverage?
3. How do perpetual DEX mechanisms differ from spot DEX?
4. What is the risk profile of leveraged positions across protocols?

## Methodology

- Funding rate simulation
- Liquidation scenario modeling
- Protocol mechanism comparison
- Risk metric analysis

## Schema

Uses `schemas/research-lab/`:
- `simulation-result.schema.json` - Funding/liquidation simulations
- `evidence-bundle.schema.json` - Compiled research evidence
- `audit-event.schema.json` - Research activity tracking

## References

- ADR-0004: Market labs directory
- EXECUTION_BOUNDARY.md: Research/execution separation
- THREAT_MODEL.md: Perp-specific risks
