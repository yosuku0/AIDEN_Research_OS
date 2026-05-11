---
task_id: PR-0002
title: Cloud AI x Local AI Role Split
task_class: governance-docs-only
risk_level: medium
status: ready
human_approval_required: true
---

# Goal
governance docs / ADR / ledger update のみを対象とし、Cloud AI と Local AI の役割分割、技術スタック選定、ハイブリッドルーティング戦略を文書化する。

# Inputs
- RS-02 Cloud AI x Local AI Role Split
- 日本語アーキテクチャ設計書（Tech Stack Matrix セクション）
- ハードウェア制約: RTX 4070 Ti 12GB（実効 ~10.8GB）

# In Scope
- docs/governance/CLOUD_LOCAL_SPLIT.md の作成
- docs/system/TECH_STACK_MATRIX.md の作成
- docs/adr/ADR-0005-cloud-local-role-split.md の作成
- research/ledgers/decision-log.md の DL-0002 エントリ追加
- research/ledgers/open-questions.md のフォローアップ項目追加

# Out of Scope
- Ollama や vLLM の実際のインストール・設定
- LiteLLM Proxy の構成ファイル作成
- モデルのダウンロードや量子化
- パッケージインストール
- ランタイムコード

# Allowed Files
- docs/governance/CLOUD_LOCAL_SPLIT.md
- docs/system/TECH_STACK_MATRIX.md
- docs/adr/ADR-0005-cloud-local-role-split.md
- research/ledgers/decision-log.md
- research/ledgers/open-questions.md

# Required Outputs
1. docs/governance/CLOUD_LOCAL_SPLIT.md
   - Cloud AI scope: Deep Research, counter-evidence, policy drafting, ADR draft
   - Local AI scope: summarization, classification, routing, offline fallback
   - Routing: Local first, Cloud escalates, neither has execution authority
   - Models: Ollama (Llama 3.1 8B, Qwen2.5 7-14B) local; Claude/GPT escalate only
   - Cost: LiteLLM Proxy with budget limits
2. docs/system/TECH_STACK_MATRIX.md
   - LangGraph (primary), CrewAI (prototype only)
   - Ollama (primary), vLLM (future)
   - FastMCP (standard)
   - LiteLLM Proxy (routing)
   - LangGraph interrupt() (HITL)
   - Firecracker microVM (future sandbox)
   - Langfuse self-hosted (observability)
3. docs/adr/ADR-0005-cloud-local-role-split.md
4. Ledger updates

# Acceptance Criteria
- すべての出力ファイルが存在する
- 役割分割が明確
- ハードウェア制約が反映されている
- いずれも実行権限を持たないことが明記されている
