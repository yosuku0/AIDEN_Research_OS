# TEMPLATE_REF — governance_template 同期記録

このファイルは `AIDEN Research OS` が `governance_template` のどのバージョンを
基準にしているかを記録します。

---

## 同期元リポジトリ

- **リポジトリ**: governance_template（MIT License / yosuku0）
- **URL**: https://github.com/[owner]/governance_template

---

## 同期履歴

| 日付 | 同期バージョン（tag or commit） | 同期内容サマリー | 担当 | ADR参照 |
|---|---|---|---|---|
| 2026-05-10 | initial | 初期テンプレートからAIDEN Research OSを構築 | Human | ADR-0001 |

---

## AIDEN 側の拡張（template に存在しない要素）

以下はAIDEN Research OSが独自に追加した設計です。
`governance_template` への同期時に上書きされないよう注意してください。

### スキーマ拡張

| スキーマ | AIDEN追加フィールド |
|---|---|
| `approval-record.schema.json` | `linked_phase_gate` |
| `decision-log.schema.json` | `linked_codex_task`, `alternatives`, `consequences` |
| `risk-ledger.schema.json` | `mitigation_controls` を `array` 型に修正（templateは `string`） |

### AIDEN固有ファイル

- `docs/adr/ADR-0001〜0017/` — AIDEN 17フェーズADR群
- `docs/security/` — AIDEN固有セキュリティ設計
- `docs/system/` — AIDEN固有システム境界
- `codex/tasks/PR-0001〜0017/` — AIDEN固有タスク定義
- `fixtures/` — AIDEN固有テストフィクスチャ
- `labs/` — マーケットラボスキャフォールド
- `SAFETY.md` — AIDEN固有ハードバン10条（templateは7条）

---

## 次回同期予定

- governance_template の CI/スキーマ修正が完了した時点で同期を実施する
- 同期は `codex/prompts/05_sync-from-template.md` のプロンプトを使用する
- 破壊的変更がある場合は Human 承認を得てから適用する
