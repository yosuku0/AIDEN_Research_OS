# Codex プロンプトライブラリ — AIDEN Research OS

> このディレクトリはOpenAI Codex appで再利用可能なタスクプロンプトを格納します。
> GitHub Issueの本文またはCodexのタスク指示欄に貼り付けて使用してください。
> 各プロンプトは `AGENTS.md` の実行プロトコルに準拠しています。

---

## プロンプト一覧

| ファイル | 用途 |
|---|---|
| `01_new-adr.md` | 新しいADRとdecision-logエントリの作成 |
| `02_update-ledger.md` | 既存台帳エントリの更新・追加 |
| `03_new-phase-task.md` | 新しいCodexフェーズタスクの定義 |
| `04_security-scan.md` | ガバナンスアーティファクトのセキュリティ検証 |
| `05_sync-from-template.md` | governance_templateからの差分同期 |

---

## 01_new-adr.md — 新しいADR作成プロンプト

```
タスク: 新しいArchitecture Decision Recordを作成する

## 入力情報（以下を埋めてから実行）
- ADR番号: ADR-XXXX
- タイトル: [タイトルを記述]
- 決定内容: [何を決めるか]
- 背景: [なぜこの決定が必要か]
- 却下した代替案: [代替案A / 代替案B]
- リスク: [残存リスク]
- 関連フェーズ: PR-XXXX

## 実行手順（Codexへの指示）

1. AGENTS.md を読み、実行プロトコルを確認する
2. SAFETY.md のハードバン10条を確認する
3. 既存のADR番号を確認する:
   ls docs/adr/ | sort | tail -5
4. 以下のファイルを作成する:
   docs/adr/ADR-XXXX-[kebab-case-title].md
   （ADR作成ルールに従ったフォーマットで記述）
5. research/ledgers/decision-log.md に DL-XXXX エントリを追加する
   （既存の最大IDを確認してからインクリメント）
6. docs/governance/PHASE_ARTIFACT_MANIFEST.md の該当フェーズ行を更新する
7. 作業前後のセキュリティチェックを実行する
8. PR を作成する（ブランチ名: codex/ADR-XXXX-[short-title]）

## 禁止事項
- 認証情報・ローカルパス・rawログをADRに含めない
- フェーズゲートを hold → go に変更しない
- SAFETY.md を変更しない

## 完了条件
- [ ] docs/adr/ADR-XXXX-*.md が作成された
- [ ] decision-log.md に対応エントリが追加された
- [ ] JSON Schemaチェックがパスした
- [ ] セキュリティスキャンがクリーンだった
```

---

## 02_update-ledger.md — 台帳更新プロンプト

```
タスク: 指定された台帳エントリを追加・更新する

## 入力情報（以下を埋めてから実行）
- 対象台帳: [decision-log / risk-ledger / approval-record / phase-gate-record / incident-record]
- 操作: [追加 / 更新]
- エントリID: [DL-XXXX / RK-XXXX / AR-XXXX / PG-XXXX / IR-XXXX]
- 変更内容: [何を追加・変更するか]

## 実行手順（Codexへの指示）

1. AGENTS.md を読み、台帳エントリ記述ルールを確認する
2. docs/governance/LEDGER_SCHEMA.md を読み、スキーマを確認する
3. 対象台帳ファイルを読む:
   cat research/ledgers/[target].md
4. 既存のIDを確認してから新IDを決定する（重複禁止）
5. Markdownテーブルにエントリを追加または更新する
6. 追加したエントリが LEDGER_SCHEMA の形式に準拠していることを確認する
7. 必要に応じて関連台帳も更新する（例: decision-log 追加 → evidence-ledger も）
8. セキュリティチェックを実行する
9. PR を作成する（ブランチ名: codex/ledger-[entry-id]）

## リスク台帳更新時の severity/likelihood 制約
- severity: low / medium / high / critical のみ
- likelihood: low / medium / high のみ
- mitigation_controls: セミコロン区切りの文字列（複数制御をリスト化）

## 禁止事項
- フェーズゲートを hold → go に変更しない（Humanのみ）
- approval-record の decision を pending 以外に変更しない（Humanのみ）
- 認証情報をエントリに含めない

## 完了条件
- [ ] 対象台帳が更新された
- [ ] ID重複がない
- [ ] LEDGER_SCHEMA 準拠を確認した
- [ ] セキュリティスキャンがクリーンだった
```

---

## 03_new-phase-task.md — 新規フェーズタスク定義プロンプト

```
タスク: 新しい Codex フェーズタスクを定義する

## 入力情報（以下を埋めてから実行）
- タスクID: PR-XXXX
- タスク名（kebab-case）: [task-name]
- タスクタイトル: [日本語タイトル]
- ゴール: [このタスクで達成すること]
- スコープ: [in_scope / out_of_scope]
- 許可ファイルパターン: [例: docs/**, schemas/**, research/ledgers/**]
- 禁止ファイルパターン: [例: src/**, runtime/**, .env]
- 必須アウトプット: [生成すべきファイルリスト]
- リスクレベル: [Low / Medium / High / Critical]

## 実行手順（Codexへの指示）

1. AGENTS.md を読み、実行プロトコルを確認する
2. SAFETY.md のハードバン10条を確認する
3. 既存タスクのIDを確認する:
   ls codex/tasks/ | sort | tail -5
4. 新しいタスクディレクトリとファイルを作成する:
   mkdir -p codex/tasks/PR-XXXX-[task-name]/
   cat > codex/tasks/PR-XXXX-[task-name]/task.md << 'EOF'
   （task-template.md の20フィールドを全て埋める）
   EOF
5. research/ledgers/phase-gate-record.md に PG-XXXX エントリを追加する:
   | PG-XXXX | RS-XX | hold | [タスク名]が生成され、Humanレビュー待ち | Human | pending | PR-XXXX; approval-record.md | No execution authority granted. | pending |
6. docs/governance/PHASE_ARTIFACT_MANIFEST.md に行を追加する
7. research/ledgers/task-promotion-record.md に TP-XXXX エントリを追加する
8. PR を作成する（ブランチ名: codex/PR-XXXX-[task-name]）

## task.md の prohibited_work 必須文言
以下を必ず prohibited_work に含める:
"Do not store credential values or local secret paths.
 Do not create executable runtime code.
 Do not grant AI approval, signing, deploy, transfer, bridge, swap,
 or production-write authority."

## 完了条件
- [ ] codex/tasks/PR-XXXX-*/task.md が作成された（20フィールド全て記入）
- [ ] phase-gate-record に PG-XXXX (hold) が追加された
- [ ] PHASE_ARTIFACT_MANIFEST に行が追加された
- [ ] task-promotion-record に TP-XXXX が追加された
- [ ] セキュリティスキャンがクリーンだった
```

---

## 04_security-scan.md — セキュリティ検証プロンプト

```
タスク: ガバナンスアーティファクトのセキュリティ検証を実行する

## 用途
- PRマージ前の最終チェック
- 定期的なセキュリティ監査
- 新しいコントリビューターのオンボーディング前確認

## 実行手順（Codexへの指示）

1. AGENTS.md のテスト・検証コマンドを全て実行する

2. 追加チェック: 台帳エントリのプレースホルダー残存確認
   grep -rI "replace before use\|PLACEHOLDER\|TODO\|FIXME\|your-.*-here" \
     research/ledgers/ codex/tasks/ --include="*.md" \
     && echo "WARNING: unresolved placeholders" || echo "OK: no placeholders"

3. JSON Schema 整合性チェック（台帳と対応スキーマの照合）
   python3 << 'EOF'
   import json, glob

   schema_fields = {}
   for f in glob.glob('schemas/**/*.json', recursive=True):
       s = json.load(open(f))
       name = f.split('/')[-1].replace('.schema.json', '')
       schema_fields[name] = list(s.get('properties', {}).keys())

   for name, fields in schema_fields.items():
       ledger = f'research/ledgers/{name}.md'
       try:
           lines = open(ledger).readlines()
           header_line = next(l for l in lines if l.startswith('|'))
           headers = [h.strip() for h in header_line.split('|') if h.strip()]
           missing = [f for f in fields if f not in headers]
           extra = [h for h in headers if h not in fields and h != 'id']
           if missing:
               print(f'SCHEMA→LEDGER gap in {name}: schema has {missing} but ledger header missing')
           if extra:
               print(f'LEDGER→SCHEMA gap in {name}: ledger has {extra} but schema missing')
           if not missing and not extra:
               print(f'OK: {name}')
       except (StopIteration, FileNotFoundError):
           print(f'SKIP: {ledger} not found or no table')
   EOF

4. 禁止ファイルチェック
   for pattern in "runtime" "src" "apps" "package.json" \
                  "package-lock.json" "yarn.lock" "Dockerfile"; do
     found=$(find . -path "./.git" -prune -o -name "$pattern" -print | grep -v ".git")
     [ -n "$found" ] && echo "ERROR: forbidden: $found" || true
   done

5. ADR セクション必須チェック
   python3 << 'EOF'
   import os, glob
   required_sections = ['## Status', '## Context', '## Decision', '## Consequences']
   for f in glob.glob('docs/adr/ADR-*.md'):
       content = open(f).read()
       missing = [s for s in required_sections if s not in content]
       if missing:
           print(f'ADR INCOMPLETE: {f} missing: {missing}')
       else:
           print(f'OK: {f}')
   EOF

6. 全チェック結果をまとめてレポートする
7. 問題があれば risk-ledger.md に新規 RK エントリを追加する
8. PR を作成する（ブランチ名: codex/security-scan-[YYYY-MM-DD]）

## 完了条件
- [ ] 全6ステップのチェックが実行された
- [ ] 問題がある場合は RK エントリが追加された
- [ ] チェック結果のサマリーがPRに記載された
```

---

## 05_sync-from-template.md — governance_template 同期プロンプト

```
タスク: governance_template リポジトリからの変更を AIDEN Research OS に取り込む

## 前提確認
- TEMPLATE_REF.md に記載された同期元バージョンを確認する
- 同期するファイルは「共通パターン」のみ（AIDEN固有の拡張は上書きしない）

## 実行手順（Codexへの指示）

1. TEMPLATE_REF.md を読み、前回同期バージョンと変更内容を確認する

2. 同期対象ファイルを特定する（以下が候補）:
   - schemas/governance/*.schema.json（フィールド追加・型修正）
   - codex/templates/task-template.md（フィールド追加）
   - codex/templates/pr-audit-template.md（チェックリスト追加）
   - .github/ISSUE_TEMPLATE/*.yml（バリデーション強化）
   - .github/workflows/governance-ci.yml（チェック強化）

3. 各ファイルについて差分を確認する（上書きではなくマージ）:
   - governance_template の変更内容を理解する
   - AIDEN Research OS 側の拡張（例: linked_phase_gate, minLength 追加済み）を保持する
   - 破壊的変更（required フィールドの追加など）は SKIP して Human に報告する

4. schema 同期時のルール:
   - AIDEN が追加した拡張フィールド（linked_phase_gate など）は削除しない
   - template 側で型修正があった場合（string→array など）は AIDEN 側も同様に修正する
   - minLength の追加は安全（破壊的変更ではない）→ 適用する
   - required への新フィールド追加は破壊的 → Human 承認後のみ適用

5. TEMPLATE_REF.md を更新する:
   - 同期バージョン・日付・変更サマリーを記録する

6. research/ledgers/decision-log.md に同期記録エントリを追加する

7. PR を作成する（ブランチ名: codex/sync-template-[version]）
   PR説明に「同期内容」「スキップした項目とその理由」を明記する

## 破壊的変更の判断基準
以下に該当する変更は Human 承認が必要:
- required フィールドへの新規追加
- enum 値の削除
- additionalProperties の false → true への変更
- 既存フィールドの型変更（string → object など）

## 完了条件
- [ ] 全同期対象ファイルの差分が確認された
- [ ] 破壊的変更はスキップされHumanに報告された
- [ ] TEMPLATE_REF.md が更新された
- [ ] decision-log に同期記録が追加された
- [ ] CI チェックがパスした
```
