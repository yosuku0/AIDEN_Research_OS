# SECRET_MANAGER_SELECTION

## Purpose

Evaluate secret manager candidates and select a future approach without implementing runtime custody.

## Evaluation Criteria

Criteria are security, recovery, purge capability, credential rotation support, operational complexity, auditability, and fit with Human approval gates.

## Candidate Evaluation

| Candidate | Security | Recovery | Purge capability | Credential rotation | Decision |
|---|---|---|---|---|---|
| OS keychain | Strong local platform custody | Platform-supported | Strong | Good | Selected primary future candidate |
| Local encrypted vault | Strong if operated correctly | User-managed | Good | Good | Selected secondary future candidate |
| Password manager | Strong workflow support | Product-dependent | Good | Good | Hold |
| Cloud secret manager | Strong but provider-dependent | Provider-managed | Good | Good | Rejected as default |
| Hardware-backed storage | Strong | Operationally complex | Good | Medium | Future review |
| Plaintext file | Poor | Poor | Poor | Poor | Never |

## Selected Approach

OS keychain is primary and local encrypted vault is secondary. This selection does not approve implementation, secret retrieval, secret storage, provider integration, or runtime code.

## Rejected Approaches

Cloud secret manager is rejected as default due provider dependency. Plaintext file is never allowed.


## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md, research/ledgers/approval-record.md.
