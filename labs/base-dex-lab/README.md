# Base DEX Lab

## Purpose

Research lab for analyzing Base chain DEX (Decentralized Exchange) protocols, liquidity patterns, swap mechanics, and market structure. This is a documentation-only research artifact within AIDEN Research OS.

## Boundary

This lab is a research scaffold, not a trading implementation. It grants no signing, deployment, capital, swap, bridge, transfer, or production-write authority. All outputs are governance artifacts (documentation, schemas, fixtures, evidence bundles).

## Research Questions

1. How is liquidity distributed across Base DEX pools?
2. What swap routing patterns are most common?
3. How do fee tiers affect trading volume?
4. What is the relationship between TVL and trading efficiency?

## Methodology

- On-chain data analysis (simulated/aggregated)
- Liquidity pool comparison
- Swap routing simulation
- Fee structure analysis

## Schema

Uses schemas from `schemas/research-lab/`:
- `audit-event.schema.json` - Track research activities
- `simulation-result.schema.json` - Store simulation outcomes
- `evidence-bundle.schema.json` - Compile evidence

## Evidence

See `fixtures/research-lab/` for sample evidence bundles.

## References

- ADR-0004: Market labs directory structure
- PRODUCT_BOUNDARY.md: Research-only boundary
- EXECUTION_BOUNDARY.md: No execution authority
