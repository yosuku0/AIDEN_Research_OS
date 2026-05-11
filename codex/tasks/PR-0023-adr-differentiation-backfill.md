# PR-0023: ADR Differentiation Backfill

## task_name

ADR Differentiation Backfill (Remaining 15 ADRs)

## task_description

Differentiate Risks and Follow-ups sections for remaining ADRs: 0001, 0002, 0003, 0004, 0006, 0007, 0008, 0009, 0010, 0012, 0013, 0014, 0015, 0016, 0017. ADR-0005 and ADR-0011 are already done.

## boundary_scope

Documentation quality improvement. No decision changes, no runtime impact.

## allowed_files

- docs/adr/ADR-0001 through ADR-0017 (Risks and Follow-ups sections ONLY)
- docs/governance/ADR_DIFFERENTIATION_GUIDE.md (read-only reference)

## forbidden_files

- ADR Status, Context, Decision, Rejected Alternatives sections (read-only)
- Any non-ADR file
- Any schema or ledger file

## human_approval

TRUE

## required_outputs

- Each updated ADR has 2+ ADR-specific risks (concrete, not vague)
- Each updated ADR has 2+ specific follow-up actions (with linked OQ/ledger where applicable)
- Each updated ADR references ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks

## priority_order

Process in this order:
1. ADR-0014 (Secret Manager Selection) - active decision area
2. ADR-0016 (OS Keychain Boundary) - upcoming implementation
3. ADR-0008 (AIDEN Runtime Boundary) - core security boundary
4. ADR-0010 (MCP Boundary) - tool permission model
5. ADR-0001, 0002, 0003, 0004, 0006, 0007, 0009, 0012, 0013, 0015, 0017

## per_adr_template

Replace ONLY these sections in each ADR:

```markdown
## Risks

- [ADR-specific risk 1: concrete, specific to this ADR's decision scope]
- [ADR-specific risk 2: concrete, specific to this ADR's decision scope]
- See docs/governance/ADR_DIFFERENTIATION_GUIDE.md for cross-cutting risks

## Follow-ups

- [Specific action 1 with linked open-question or ledger entry]
- [Specific action 2 with linked open-question or ledger entry]
- Review at phase gates; keep linked ledgers current
```

## validation_steps

- Confirm Decision section is UNCHANGED in each ADR
- Confirm Context section is UNCHANGED
- Confirm Rejected Alternatives section is UNCHANGED
- Confirm each ADR has 2+ specific risks and 2+ specific follow-ups
- Confirm cross-cutting risk reference is present
- Run `scripts/validate-governance.sh` passes

## incident_trigger

If any ADR's Decision, Context, or Rejected Alternatives sections are modified, STOP and create incident-record.md entry. These sections must remain untouched.

## rollback_plan

1. For each modified ADR, revert Risks and Follow-ups to pre-task state
2. Update decision-log.md if entries were added

## linked_ledger

INC-005 (H-005 resolution)
