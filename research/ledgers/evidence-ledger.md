# evidence-ledger

## Schema Reference

docs/governance/LEDGER_SCHEMA.md

## Entries

| id | source_type | source_summary | linked_decision | confidence | notes |
|---|---|---|---|---|---|
| EV-0001 | architecture prompt | Master scaffold prompt summarized into reviewed artifacts | DL-0001 | high | Raw prompt is not canonical. |
| EV-0002 | LangGraph documentation | Durable execution, checkpointing, and interrupt-based HITL patterns inform ADR-0011. | DL-0002 | medium | Use reviewed summaries only. |
| EV-0003 | MCP specification | Host-client-server separation, authorization ownership, roots as advisory context, and tool permission boundaries inform ADR-0010. | DL-0002 | medium | Use reviewed summaries only. |
| EV-0004 | OpenAI Codex documentation | Isolated task execution and artifact-driven implementation worker boundaries inform Codex task templates. | DL-0001 | medium | Use reviewed summaries only. |
| EV-0005 | GitHub documentation | Protected branches, CODEOWNERS, issue forms, pull request templates, and workflow files inform ADR-0002. | DL-0001 | medium | Use reviewed summaries only. |
| EV-0006 | Base documentation | Public endpoint limitations and Flashblocks references inform market-lab boundary notes. | DL-0001 | medium | Base DEX Lab remains one market domain only. |
| EV-0007 | FastMCP documentation | Tool registration, transport, and auth middleware references inform TECH_STACK_MATRIX and MCP boundary docs. | DL-0002 | medium | No MCP server implementation in this phase. |
| EV-0008 | LiteLLM documentation | Budget controls and routing references inform CLOUD_LOCAL_SPLIT and MODEL_ROUTING_COST_LIMITS. | DL-0002 | medium | No provider integration in this phase. |
