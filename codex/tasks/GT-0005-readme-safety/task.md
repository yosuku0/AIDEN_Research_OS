# GT-0005: governance_template — README と SAFETY_TEMPLATE の改訂

## task_id
GT-0005-readme-safety

## title
governance_template の README Getting Started を8ステップに改訂し
SAFETY_TEMPLATE.md にリネーム指示を追記する

## status
draft

## human_approval_required
false

## task_class
governance

## risk_level
Low

## goal
採用者が governance_template を Fork したときに踏む落とし穴を除去する。
具体的には:
1. README の Getting Started を8ステップに拡充（CODEOWNERS解決・SAFETY.mdリネーム・
   ブランチ保護・プレースホルダー除去の手順を明記）
2. SAFETY_TEMPLATE.md 冒頭に「このファイルを SAFETY.md にリネームしてください」という
   アダプション指示を追記

## background
監査レポート HIGH-T1（SAFETY_TEMPLATE.md 命名トラップ）の対応。
README には「Replace placeholder owner and project names」しか書かれておらず、
SAFETY_TEMPLATE.md のリネームや CODEOWNERS の解決が抜けている。

## inputs
- 監査レポート HIGH-T1 / README の Getting Started 現行版
- governance_template/README.md（現行）
- governance_template/SAFETY_TEMPLATE.md（現行）

## in_scope
- `governance_template/README.md` の Getting Started セクション更新
- `governance_template/SAFETY_TEMPLATE.md` 冒頭へのアダプション指示追記

## out_of_scope
- README の他セクション（Use This For / Do Not Use This For）の変更
- SAFETY_TEMPLATE.md の Hard Bans 内容の変更
- スキーマ・CI の変更

## allowed_files
governance_template/README.md
governance_template/SAFETY_TEMPLATE.md

## forbidden_files
governance_template/schemas/**
governance_template/docs/**
governance_template/research/**
governance_template/.github/**
governance_template/codex/**

## required_outputs
- governance_template/README.md（Getting Started を8ステップに更新）
- governance_template/SAFETY_TEMPLATE.md（冒頭にアダプション手順を追記）

## prohibited_work
Hard Bans の内容を変更しない。
認証情報・ローカルパス・実行コードを含めない。
Use This For / Do Not Use This For セクションを変更しない。

## implementation_notes

### README.md の Getting Started セクション（差分）

現行:
```markdown
## Getting Started

1. Copy this template into a private project repository.
2. Replace placeholder owner and project names.
3. Fill in product boundary and approval flow.
4. Define allowed and forbidden files for each task.
5. Keep raw inputs outside the repository and promote redacted summaries only.
```

修正後:
```markdown
## Getting Started

1. Copy this template into a private project repository.
2. **`SAFETY_TEMPLATE.md` を `SAFETY.md` にリネームし**、
   プロジェクト固有のハードバンを記述する。
3. **`.github/CODEOWNERS` の `PLACEHOLDER_OWNER`** を
   実際の GitHub ユーザー名に置き換える。
4. **GitHub Settings → Branches → main でブランチ保護を有効化する。**
   "Require review from Code Owners" をオンにする。
5. `docs/governance/` のドキュメントに
   プロジェクト名・製品境界・承認フローを記入する。
6. 各 Codex タスクに `allowed_files` と `forbidden_files` を定義する。
7. **`research/ledgers/` のプレースホルダー行を実際のエントリに置き換える。**
   （`replace before use` という文字列が残っていないことを確認する）
8. ローカルの raw 入力はリポジトリの外に置き、
   リダクション済みのサマリーのみをプロモートする。
```

---

### SAFETY_TEMPLATE.md 冒頭への追記（差分）

現行の先頭:
```markdown
# Safety Template
```

修正後（先頭に追記）:
```markdown
# Safety Template

> **アダプション手順**: このファイルを `SAFETY.md` にリネームしてから使用してください。
> リネーム後、下記の Hard Bans をプロジェクト固有の禁止事項に更新してください。
> `SAFETY_TEMPLATE.md` という名前のままでは、ガバナンス CI の必須ファイルチェックが
> `SAFETY.md` を要求する場合に失敗します。

```

その後に既存の `## Hard Bans` セクションが続く（変更なし）。

## tests_or_checks

```bash
# README に8ステップが含まれるか確認
step_count=$(grep -c "^[0-9]\." governance_template/README.md || echo 0)
echo "Getting Started steps: $step_count"
[ "$step_count" -ge 8 ] && echo "OK: 8+ steps" || echo "WARNING: fewer than 8 steps"

# README に SAFETY.md リネーム指示が含まれるか
grep -q "SAFETY.md" governance_template/README.md \
  && echo "OK: SAFETY.md rename mentioned" \
  || echo "MISSING: SAFETY.md rename instruction"

# README に PLACEHOLDER_OWNER 解決指示が含まれるか
grep -q "PLACEHOLDER_OWNER\|CODEOWNERS" governance_template/README.md \
  && echo "OK: CODEOWNERS mentioned" \
  || echo "MISSING: CODEOWNERS instruction"

# SAFETY_TEMPLATE.md にアダプション指示が含まれるか
grep -q "アダプション手順\|SAFETY.md" governance_template/SAFETY_TEMPLATE.md \
  && echo "OK: adoption note present" \
  || echo "MISSING: adoption note"

# Hard Bans が維持されているか（7条）
ban_count=$(grep -c "^[0-9]\. Do not" governance_template/SAFETY_TEMPLATE.md || echo 0)
echo "Hard Bans count: $ban_count"
[ "$ban_count" -ge 7 ] && echo "OK: bans intact" || echo "WARNING: bans may be reduced"
```

## acceptance_criteria
- [ ] README の Getting Started が8ステップになっている
- [ ] README に `SAFETY.md` へのリネーム指示がある
- [ ] README に `CODEOWNERS` の `PLACEHOLDER_OWNER` 解決指示がある
- [ ] README にブランチ保護の有効化手順がある
- [ ] README にプレースホルダー除去の確認手順がある
- [ ] `SAFETY_TEMPLATE.md` 冒頭にアダプション指示が追記されている
- [ ] Hard Bans の内容（7条）が変更されていない

## review_checklist
- Hard Bans 内容が変更されていないこと
- 認証情報・ローカルパスなし
- 追加以外のセクション変更なし

## rollback_plan
`README.md`・`SAFETY_TEMPLATE.md` を Git で revert してPRを閉じる。
