# LangGraph HITL Workflow (Concrete)

## Purpose

Concrete workflow specification for LangGraph Human-in-the-Loop (HITL) approval system, based on ADR-0011.

## StateGraph Nodes

```
[Start] -> [ArtifactCreation] -> [RedactionCheck] -> [HumanApprovalGate]
                                                              |
                                    [Approve] <--------------|
                                        |
                                        v
                                    [LedgerUpdate] -> [CodexTask] -> [End]
                                        |
                                    [Hold] <--------------|
                                        |
                                        v
                                    [WaitForHuman] -------> [HumanApprovalGate]
                                        |
                                    [Reject] <--------------|
                                        |
                                        v
                                    [IncidentRecord] -> [Rollback] -> [End]
```

## Node Definitions

### ArtifactCreation
- Type: Standard node
- Function: Create governance artifact (ADR, schema, fixture)
- Output: Unreviewed artifact

### RedactionCheck
- Type: Standard node
- Function: Verify no secrets, credentials, or execution authority
- Validation: `scripts/validate-governance.sh` secret-scan
- Output: Redacted artifact or reject

### HumanApprovalGate
- Type: HumanApproval node (interrupt)
- Checkpoint: Save state before interrupt
- Timeout: 7 days (configurable per APPROVAL_FLOW.md)
- Options: Approve, Hold, Reject

### LedgerUpdate
- Type: Standard node
- Function: Update approval-record.md with decision
- Required: approval_criteria_met field

### WaitForHuman
- Type: Standard node
- Function: Pause workflow, notify approver
- Persistence: SQLite checkpoint (future: Postgres)

### IncidentRecord
- Type: Standard node
- Function: Create incident-record.md entry
- Trigger: Rejection with boundary drift detected

## Checkpoint Persistence Strategy

| Phase | Implementation | When |
|---|---|---|
| Current | InMemorySaver | Development only |
| Short-term | SQLiteSaver | Single-approver workflows |
| Long-term | PostgresSaver | Multi-approver production |

## Interrupt Configuration

```python
# Interrupt before HumanApprovalGate for all approval types
workflow.add_node("HumanApprovalGate", human_approval_node)
workflow.add_conditional_edges(
    "HumanApprovalGate",
    route_approval,
    {"approve": "LedgerUpdate", "hold": "WaitForHuman", "reject": "IncidentRecord"}
)
```

## Timeout Handling

| Approval Type | Timeout | Action on Timeout |
|---|---|---|
| Phase artifact | 7 days | Auto-hold, notify owner |
| CI security | 3 days | Auto-hold, escalate |
| Schema migration | 5 days | Auto-hold, notify |
| ADR differentiation | 7 days | Auto-hold |

## Rollback Triggers

1. Secret detected in output -> Immediate reject
2. Forbidden file modified -> Reject + incident
3. Boundary drift detected -> Reject + incident
4. Approver unavailable (2x timeout) -> Escalate to alternate approver

## References

- ADR-0011: LangGraph HITL workflow
- HITL_APPROVAL_DESIGN.md: Approval design
- APPROVAL_FLOW.md: Checklist and state transitions
