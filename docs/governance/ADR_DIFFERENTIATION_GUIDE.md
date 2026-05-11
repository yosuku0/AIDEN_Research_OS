# ADR_DIFFERENTIATION_GUIDE

## Purpose

Prevent mechanical copy-paste in ADR Risk and Follow-up sections. Each ADR MUST have context-specific content that reflects its unique decision scope.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Policy

### Cross-Cutting Risks (Extracted Common Pattern)

The following generic risks apply to ALL ADRs and should NOT be repeated individually. Instead, reference this document:

> See docs/governance/ADR_DIFFERENTIATION_GUIDE.md - Cross-cutting risks: documentation drift, approval semantic ambiguity, execution system confusion.

### Per-ADR Risk Differentiation Rules

Each ADR's `## Risks` section MUST include:

1. **At least 2 ADR-specific risks** that would NOT apply to any other ADR
2. A reference to cross-cutting risks (not the full text)
3. Risks should be concrete, not vague ("may drift" is insufficient)

### Per-ADR Follow-up Differentiation Rules

Each ADR's `## Follow-ups` section MUST include:

1. **At least 2 ADR-specific follow-up actions** with linked open-questions or ledger entries where applicable
2. Concrete next steps, not generic "review at phase gates"
3. A reference to cross-cutting follow-ups

### Example: ADR-0005 (Cloud Local Split) - Differentiated Version

```markdown
## Risks

- Cloud model provider failure may stall all high-precision synthesis tasks with no documented fallback path
- Local model misclassification may incorrectly route complex tasks to local inference, degrading output quality
- Budget threshold ambiguity (OQ-0002) may cause either excessive cloud spend or premature workflow holds
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks

## Follow-ups

- Define concrete budget thresholds (OQ-0002) before phase gate PG-0002 closes
- Validate local model list (Llama 3.1 8B, Qwen2.5 7-14B, Phi-4 14B) against target workstation (RTX 4070 Ti 12GB)
- Review cloud provider failover options within budget constraints
- Review at phase gates; keep linked ledgers current
```

### Example: ADR-0011 (LangGraph HITL) - Differentiated Version

```markdown
## Risks

- Checkpoint persistence migration (InMemory -> SQLite -> Postgres) may lose approval state if migration is not versioned
- LangGraph API changes between v1.0 and future versions may break interrupt-based HITL workflow compatibility
- Timeout handling without checkpoint persistence may lose in-progress Human approval context
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks

## Follow-ups

- Evaluate PostgresSaver vs SQLite durability trade-offs (OQ-0001) before production readiness gate
- Track LangGraph v1.x changelog for breaking changes to interrupt() API
- Define timeout duration policy for each approval node type
- Review at phase gates; keep linked ledgers current
```

## Backfill Target ADRs

The following ADRs require Risk/Follow-up differentiation (audit finding H-005):

| ADR | Topic | Specific Risk Direction |
|---|---|---|
| ADR-0001 | Product identity | Single-bot framing confusion, Base-only identity drift |
| ADR-0002 | GitHub source of truth | Offline work desync, CODEOWNERS misconfiguration |
| ADR-0003 | Monorepo topology | Premature repo split, inter-repo dependency management |
| ADR-0004 | Market labs directory | Lab-to-implementation scope creep, cross-lab inconsistency |
| ADR-0005 | Cloud local split | Provider failure, local misclassification, budget ambiguity |
| ADR-0006 | Governance ledger schema | Schema version drift, ledger non-compliance |
| ADR-0007 | Runtime integration boundary | Research-to-runtime shortcut, API boundary bypass |
| ADR-0008 | AIDEN runtime boundary | Orchestrator scope creep, credential custody temptation |
| ADR-0009 | Security test plan | Test plan becoming stale, executable test delay |
| ADR-0010 | MCP boundary tool permission | Tool permission escalation, server-side auth override |
| ADR-0011 | LangGraph HITL workflow | Checkpoint migration risk, API compatibility, timeout loss |
| ADR-0012 | Local storage credential rotation | Raw artifact retention beyond policy, purge failure |
| ADR-0013 | Credential rotation execution | Rotation procedure not followed, Human unavailability |
| ADR-0014 | Secret manager selection | Selected candidate deprecation, secondary candidate inadequacy |
| ADR-0015 | Secret manager narrow plan | Scope creep within narrow plan, premature adapter approval |
| ADR-0016 | OS keychain adapter boundary | Adapter scope creep to secret retrieval, platform incompatibility |
| ADR-0017 | Secret manager minimal implementation | Schema-only illusion of security, fixture inadequacy |

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md
