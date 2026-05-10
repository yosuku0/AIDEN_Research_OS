# TECH_STACK_MATRIX

## Purpose

Records technology choices from the architecture design.

## Boundary

This artifact is part of the AIDEN Research OS research/control-plane scaffold. It grants no signing, deployment, capital, allowlist, release, wallet, swap, bridge, transfer, or production-write authority.

## Matrix

LangGraph v1.0+ is primary orchestration; CrewAI is prototyping only. Ollama is primary local inference; vLLM is future scale. FastMCP Python is MCP standard. LiteLLM Proxy is unified cloud exit. LangGraph interrupt() is HITL. Firecracker microVM is future sandboxing. Langfuse self-hosted is observability.

## Model References

Local: Llama 3.1 8B Instruct Q4_K_M, Qwen2.5 7B to 14B class, Phi-4 14B class, Llama Guard 3 8B. Cloud escalation: Claude, GPT, and Gemini families through governed routing.

## Constraints

Reference hardware is RTX 4070 Ti 12GB with about 10.8GB effective VRAM. Max workflow steps: 15. Budget: 50,000 tokens or 1.00 USD per session. Loop detection compares hashes for the last three turns.

## References

Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md, docs/system/EXECUTION_BOUNDARY.md, research/ledgers/approval-record.md.
