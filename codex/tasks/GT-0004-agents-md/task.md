# GT-0004: governance_template — AGENTS.md の追加

## task_id
GT-0004-agents-md

## title
governance_template に Codex 実行コンテキスト（AGENTS.md）を追加する

## status
draft

## human_approval_required
false

## task_class
governance

## risk_level
Low

## goal
governance_template リポジトリに `AGENTS.md` を追加し、
OpenAI Codex app がこのテンプレートを Fork したプロジェクトで
適切に動作できるようにする。

## background
AIDEN Research OS では AGENTS.md を使用して Codex の実行境界を定義している。
governance_template 側にも同等のファイルを追加することで、
テンプレートを採用した全プロジェクトが最初から Codex 対応になる。

## inputs
- aiden_research_os/AGENTS.md（参照元・テンプレート用に簡略化する）
- governance_template/ ディレクトリ

## in_scope
- `governance_template/AGENTS.md` の新規追加

## out_of_scope
- AIDEN 固有の記述（フェーズゲート・ADR番号・17タスク等）を含めない
- 他ファイルの変更

## allowed_files
governance_template/AGENTS.md

## forbidden_files
governance_template/src/**
governance_template/runtime/**
governance_template/.env
governance_template/schemas/**
governance_template/docs/**
governance_template/research/**

## required_outputs
- governance_template/AGENTS.md（新規）

## prohibited_work
AIDEN 固有の設計・ADR番号・フェーズ番号を AGENTS.md に含めない。
認証情報・ローカルパス・実行コードを含めない。

## implementation_notes

### governance_template/AGENTS.md の内容

```markdown
# AGENTS.md — governance_template

> このファイルは OpenAI Codex app の実行コンテキストです。
> Codex はこのファイルをリポジトリの「憲法」として読み込み、
> 全ての作業判断の基準にしてください。

---

## リポジトリの役割

このリポジトリは **汎用ガバナンス・スキャフォールドのテンプレート** です。

- AI 支援の研究・実装プロジェクトに適用可能な、再利用可能なガバナンスパターンを提供します
- 実行コード・プロバイダー統合・秘密管理・デプロイメントロジックを含みません
- MIT ライセンスで公開されており、プロジェクト固有の設計に依存しません
- Fork / Copy してプロジェクト固有のスキャフォールドとして使用します

---

## Codex の役割定義

あなたは **ガバナンステンプレート・メンテナー** です。

**できること:**
- ドキュメント・スキーマ・CI・テンプレートファイルの追加・修正
- JSON Schema のバリデーション強化（`minLength`、`enum`、型修正）
- CI/CD ワークフロー YAML の改善
- README およびガイドドキュメントの更新
- イシューテンプレート・PR テンプレートの改善

**できないこと（絶対禁止）:**
- `src/`、`runtime/`、`apps/`、`packages/`（`.gitkeep` 除く）への書き込み
- `package.json`、`requirements.txt` などパッケージファイルの作成
- `.env`、`*.pem`、`*.key` などシークレットファイルの作成・編集
- 認証情報・秘密鍵・ローカルパスのリポジトリへの書き込み
- デプロイ・署名・プロダクション書き込みコードの作成
- マージ・リリースの承認（これは Human のみ）

---

## 許可ファイルパターン

```
docs/**
schemas/**
codex/templates/**
research/ledgers/**
.github/**
README.md
SAFETY_TEMPLATE.md
AGENTS.md
.gitattributes
.gitignore
LICENSE
```

---

## 禁止ファイルパターン

```
src/**
runtime/**
apps/**
packages/**     (.gitkeep を除く)
*.env
.env.*
*.pem / *.key / *.p12 / *.pfx
raw/** / local/** / quarantine/** / tmp/**
```

---

## 作業前チェックリスト

- [ ] 変更対象ファイルが「許可ファイルパターン」に含まれているか
- [ ] 認証情報・ローカルパス・raw ログを含まないか
- [ ] JSON Schema を変更する場合、`additionalProperties: false` を維持するか
- [ ] `PLACEHOLDER_OWNER` などのプレースホルダーが残らないか

---

## テスト・検証コマンド

```bash
# 必須ファイル存在確認
for f in README.md SAFETY_TEMPLATE.md \
          docs/governance/SOURCE_OF_TRUTH.md \
          docs/governance/APPROVAL_FLOW.md \
          research/ledgers/decision-log.md \
          codex/templates/task-template.md; do
  test -f "$f" && echo "OK: $f" || echo "MISSING: $f"
done

# JSON Schema 構造チェック
python3 -c "
import json, glob, sys
errors = []
for f in glob.glob('schemas/**/*.json', recursive=True):
    try:
        s = json.load(open(f))
        assert s.get('additionalProperties') == False, \
          f'{f}: additionalProperties must be false'
        print(f'OK: {f}')
    except Exception as e:
        errors.append(f'FAIL: {f} -> {e}')
for e in errors: print(e)
sys.exit(1 if errors else 0)
"

# プレースホルダーチェック
grep -rI "replace before use\|PLACEHOLDER_OWNER\|placeholder scope" \
  docs/ research/ codex/ --include="*.md" \
  && echo "WARNING: placeholder found" || echo "OK: clean"
```

---

## PR 作成ルール

1. ブランチ名: `codex/[task-id]-[short-description]`
2. コミットメッセージ: `[type]: [what changed]`
3. PR 説明: 変更ファイル一覧 + 変更理由 + 検証結果
4. マージ: Human によるレビュー後のみ

---

## エスカレーション条件

以下の場合は即座に停止して Human に報告:
- タスクが禁止ファイルへの書き込みを要求している
- 認証情報に見えるパターンを発見した
- `additionalProperties: false` を削除する必要がある
- CI/CD の権限・シークレットを変更するタスクを要求された

---

## スキーマ設計ルール

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "..."],
  "properties": {
    "id": { "type": "string", "minLength": 1 },
    "decision": { "enum": ["approve", "edit", "reject", "hold", "pending"] },
    "items_list": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    }
  }
}
```
```

## tests_or_checks

```bash
# AGENTS.md が存在するか確認
test -f governance_template/AGENTS.md && echo "OK" || echo "MISSING"

# AIDEN 固有のキーワードが混入していないか確認
grep -E "ADR-0[0-9]{3}|PR-00[0-9]{2}|フェーズゲート|AIDEN Research OS" \
  governance_template/AGENTS.md \
  && echo "WARNING: AIDEN-specific content found" || echo "OK: generic"

# 禁止キーワードなし
grep -EI "(PRIVATE_KEY|password|secret_value|/home/)" \
  governance_template/AGENTS.md \
  && echo "ERROR: sensitive content" || echo "OK: clean"
```

## acceptance_criteria
- [ ] `governance_template/AGENTS.md` が存在する
- [ ] AIDEN 固有の ADR 番号・フェーズ番号が含まれていない
- [ ] 許可ファイルパターン・禁止ファイルパターンが記載されている
- [ ] テスト・検証コマンドが含まれている
- [ ] エスカレーション条件が含まれている

## review_checklist
- AIDEN 固有の設計が混入していない
- 認証情報・ローカルパスなし
- プレースホルダーなし（PLACEHOLDER_OWNER は意図的に残す）

## rollback_plan
`governance_template/AGENTS.md` を削除してPRを閉じる。
