# AIDEN Research OS — Review Criteria and Acceptance Standards

## Universal Review Checklist

### For ALL file changes:
- [ ] Only allowed_files were modified (check against task scope)
- [ ] No forbidden_files were touched
- [ ] No credential values appear anywhere
- [ ] No local secret paths appear anywhere
- [ ] No real-looking secret examples in fixtures
- [ ] No executable code in docs/ or research/
- [ ] Cross-references to related artifacts exist

### For ADRs:
- [ ] Status field present (Accepted/Draft/Proposed)
- [ ] Context section explains the decision trigger
- [ ] Decision section is explicit and unambiguous
- [ ] Rejected alternatives listed with reasoning
- [ ] Consequences (positive and negative) documented
- [ ] Risks identified
- [ ] Follow-ups linked to research sprint or task IDs

### For Governance Documents:
- [ ] Purpose/scope clearly stated
- [ ] Safety constraints referenced
- [ ] "research/control-plane scaffold" disclaimer present
- [ ] Hard bans referenced or restated
- [ ] Human approval requirements explicit

### For Task Definitions (task.md):
- [ ] task_id, title, status present
- [ ] human_approval_required: true (default for all tasks)
- [ ] task_class and risk_level specified
- [ ] Goal and background explained
- [ ] in_scope and out_of_scope explicit
- [ ] allowed_files and forbidden_files listed
- [ ] required_outputs enumerated
- [ ] prohibited_work clear
- [ ] acceptance_criteria defined
- [ ] rollback_plan present
- [ ] related_research and related_adr linked

### For Ledger Updates:
- [ ] Schema version specified
- [ ] ID follows naming convention (DL-XXXX, RK-XXXX, AR-XXXX)
- [ ] Owner and reviewer assigned
- [ ] human_approval_required flag set correctly
- [ ] Linked artifacts cross-referenced
- [ ] Timestamps use YYYY-MM-DD format

### For Schemas:
- [ ] Valid JSON schema format
- [ ] No credential_value field
- [ ] No local_path field
- [ ] No provider_operation field
- [ ] No execution_approval field
- [ ] Descriptive metadata only (reference, not values)

### For Fixtures:
- [ ] Abstract labels only (no real-looking data)
- [ ] No reconstructable raw data
- [ ] Negative cases use safe wording only

## Merge Blocking Conditions

Merge MUST be blocked if ANY of the following are true:
1. approval-record.md missing for the change
2. PR comment used as canonical approval (PR comments are supporting evidence only)
3. Open incident related to the change scope
4. Missing rollback plan
5. Missing security test for security-related changes
6. Secret-like value present in any file
7. Local path value present in any file
8. Execution wording present (approval implying execution permission)
9. Scope expansion without new approval-record
10. Forbidden file edited

## Approval Semantics Verification

Verify that NO document implies:
- Research approval = execution permission
- Narrow implementation approval = secret custody permission
- Schema approval = runtime implementation permission
- Task approval = authority transfer

Approval language must always be scope-limited and explicitly state what is NOT authorized.
