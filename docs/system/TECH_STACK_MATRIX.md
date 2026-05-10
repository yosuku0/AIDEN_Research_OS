# TECH_STACK_MATRIX

## Purpose

Record architecture technology choices and their governance boundaries.

## Selection Matrix

| Layer | Primary | Secondary or Future | Decision |
|---|---|---|---|
| Orchestration | LangGraph v1.0+ | CrewAI for prototyping only | LangGraph owns production workflow design. |
| Checkpoint persistence | InMemory | SQLite, then PostgresSaver for production | Progression follows readiness gates. |
| Local inference | Ollama | vLLM for future scale | Ollama is primary local inference. |
| MCP implementation | FastMCP Python | none | FastMCP is the standard implementation candidate. |
| Hybrid routing | LiteLLM Proxy | direct provider calls rejected | Unified exit with budget controls. |
| HITL | LangGraph interrupt() | manual issue flow | Human gates interrupt restricted decisions. |
| Sandboxing | Firecracker microVM | documentation-only fixtures now | Future execution isolation, not implemented here. |
| Observability | Langfuse self-hosted | JSONL decision provenance | Traceable audit records. |

## Model References

Local: Llama 3.1 8B Instruct Q4_K_M, Qwen2.5 7B Q5_K_M, Phi-4 14B Q4_K_M, and Llama Guard 3 8B with CPU offload when needed. Cloud escalation: Claude Sonnet 4.5, GPT-5, and Gemini 2.5 Pro through governed routing only.

## Harness Engineering

Max steps limit is 15 steps per workflow. Token and cost budget is 50,000 tokens or 1.00 USD per session. Circuit breaker compares hashes over the last three turns. Audit logs use trace_id, actor, event, reasoning_trace, and governance_policy.

## Boundary

No runtime code, provider integration, package installation, deployment, signing, or production-write behavior is approved by this matrix.
