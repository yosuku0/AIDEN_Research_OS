# CODEX_OPERATING_RULES — AIDEN Research OS

> Codexが参照する運用ルール補足。AGENTS.mdと併せて読んでください。

---

## 意思決定の優先順位

```
1. SAFETY.md ハードバン（絶対不変）
2. docs/system/EXECUTION_BOUNDARY.md（実行境界）
3. 現在のタスクの allowed_files / forbidden_files
4. AGENTS.md の実行プロトコル
5. このファイルの運用ルール
```

ルール間の矛盾があれば、番号の小さいルールを優先し、Human に報告する。

---

## フェーズゲート権限マトリクス

| アクション | Codex | Human |
|---|---|---|
| フェーズゲートを `hold` に設定 | ✅ | ✅ |
| フェーズゲートを `go` に設定 | ❌ | ✅ |
| ADR を `Draft` で追加 | ✅ | ✅ |
| ADR を `Accepted` に変更 | ❌ | ✅ |
| 台帳エントリを追加 | ✅ | ✅ |
| 台帳エントリを削除 | ❌ | ✅ |
| SAFETY.md を変更 | ❌ | ✅ |
| ブランチへのマージ | ❌ | ✅ |
| CODEOWNERS を変更 | ❌ | ✅ |

---

## コミットメッセージ規則

```
<type>(<scope>): <summary>

type:
  feat     - 新しいアーティファクト・スキーマ・タスク
  fix      - 既存アーティファクトの修正
  docs     - ドキュメント更新
  chore    - CI・設定・ガバナンス管理
  ledger   - 台帳エントリ追加・更新
  adr      - ADR 追加・更新

scope:
  adr      - docs/adr/**
  gov      - docs/governance/**
  sec      - docs/security/**
  sys      - docs/system/**
  schema   - schemas/**
  task     - codex/tasks/**
  ledger   - research/ledgers/**
  ci       - .github/workflows/**
  lab      - labs/**

例:
  feat(adr): add ADR-0018-langgraph-state-backend
  ledger(adr): update decision-log with DL-0018
  fix(schema): add minLength to approval-record required fields
  chore(ci): add ADR section validation job
```

---

## 台帳同期ルール

### タスク完了時に更新が必要な台帳

| タスク種別 | 必須更新台帳 |
|---|---|
| 新ADR追加 | decision-log, phase-gate-record |
| 新タスク定義 | phase-gate-record, task-promotion-record |
| リスク発見 | risk-ledger |
| インシデント発生 | incident-record, risk-ledger |
| フェーズ完了（Human） | phase-gate-record, approval-record |
| 証拠取得 | evidence-ledger |

### 台帳エントリのID命名規則

```
DL-XXXX  decision-log
RK-XXXX  risk-ledger
AR-XXXX  approval-record
PG-XXXX  phase-gate-record
IR-XXXX  incident-record
EV-XXXX  evidence-ledger
TP-XXXX  task-promotion-record
RC-XXXX  redaction-checklist
RL-XXXX  research-ledger
OQ-XXXX  open-questions
```

XXXX は既存最大値 + 1（ゼロパディング4桁）。

---

## ドキュメント必須セクション

### governance/docs 全ファイル（docs/governance/配下）

```markdown
## Purpose
[このドキュメントの目的]

## Boundary
This artifact is part of the AIDEN Research OS research/control-plane scaffold.
It grants no signing, deployment, capital, allowlist, release, wallet, swap,
bridge, transfer, or production-write authority.

## Policy
Any expansion requires ADR update, ledger update, and Human approval.

## Procedure
[手順]

## References
Cross-references: SAFETY.md, docs/system/PRODUCT_BOUNDARY.md,
docs/system/EXECUTION_BOUNDARY.md, research/ledgers/approval-record.md.
```

### ADR ファイル（docs/adr/配下）

必須セクション: `## Status`, `## Context`, `## Decision`,
`## Rejected Alternatives`, `## Consequences`, `## Risks`, `## Follow-ups`

---

## よくある間違いと防止策

| 間違い | 防止策 |
|---|---|
| `@repo-owner` のまま CODEOWNERS を放置 | CI で grep チェック |
| フェーズゲートを Codex が go に変更 | AGENTS.md エスカレーション条件に明記 |
| Markdown台帳に空セル `\| \|` を含める | CI の台帳チェックでフラグ |
| ADR に `Status: Draft` のまま参照する | `## Status` の値を CI で確認 |
| 台帳 ID を重複させる | 追加前に `grep "DL-" research/ledgers/decision-log.md` |
| `prohibited_work` なしでタスク定義を作る | CI の task-structure チェック |

---

## governance_template への変更提案フロー

AIDEN固有の設計をgovernanece_templateに還元したい場合:

```
1. AIDEN 側で変更を確認・検証する
2. governance_template の Issue を開く（テンプレートのISSUE_TEMPLATE使用）
3. governance_template 側で Codex タスクを定義する
4. governance_template の PR → Human レビュー → マージ
5. AIDEN 側で 05_sync-from-template.md プロンプトを実行
6. TEMPLATE_REF.md を更新する
```

このフローにより、両リポジトリが同期したまま独立して発展できます。
