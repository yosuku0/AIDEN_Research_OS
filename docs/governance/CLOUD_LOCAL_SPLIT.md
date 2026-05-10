# CLOUD_LOCAL_SPLIT

## Purpose

Define the precise division of labor between Cloud AI and Local AI for AIDEN Research OS.

## Cloud AI Scope

Cloud AI handles Deep Research, counter-evidence, policy drafting, architecture review, long-form synthesis, and ADR draft work. Cloud AI is an inference service only and cannot approve, sign, deploy, write to production, handle secrets, or make final decisions.

## Local AI Scope

Local AI handles summarization, classification, routing support, offline fallback, triage, and high-frequency low-cost processing. Reference local inference uses Ollama with Llama 3.1 8B, Qwen2.5 7-14B class models, and Phi-4 14B class models.

## Routing Logic

Routing logic is local first. Local AI performs initial triage and summaries. Cloud escalates only when precision, counter-evidence, architecture review, or long-form synthesis is required. Neither route has execution authority.

## Cost Optimization

LiteLLM Proxy is the unified cloud exit point. Budgets are applied by provider, key, tag, and session. Budget exhaustion moves the workflow to Hold and requires Human review before further escalation.

## Hardware Constraints

The reference local workstation is RTX 4070 Ti 12GB with an effective budget of about 10.8GB VRAM after overhead.


## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, docs/governance/APPROVAL_FLOW.md, research/ledgers/approval-record.md.
