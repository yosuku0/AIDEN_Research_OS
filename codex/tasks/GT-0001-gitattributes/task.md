# GT-0001: governance_template — CRLF 正規化

## task_id
GT-0001-gitattributes

## title
governance_template の行末コード（CRLF）を LF に正規化する

## status
draft

## human_approval_required
false

## task_class
maintenance

## risk_level
Low

## goal
governance_template リポジトリの全ファイルが CRLF（Windows 改行）で保存されている。
`.gitattributes` を追加して LF に正規化し、CI スクリプトや `grep` での
`\r` 混入バグを防ぐ。

## background
監査で全 22 ファイルに CRLF 改行が検出された。
bash CI スクリプトで変数末尾に `\r` が混入すると、`grep -E` のパターンマッチが
破損するリスクがある。

## inputs
- 監査レポート（governance_template_Audit_Report.md）の MEDIUM-T4 項目
- governance_template/ ディレクトリ（同プロジェクト内）

## in_scope
- `.gitattributes` の新規追加

## out_of_scope
- ファイル内容の変更
- スキーマ・ドキュメントの修正

## allowed_files
governance_template/.gitattributes

## forbidden_files
governance_template/src/**
governance_template/runtime/**
governance_template/.env
governance_template/.env.*

## required_outputs
governance_template/.gitattributes（新規）

## prohibited_work
ファイル内容を変更しない。`.gitattributes` の追加のみ。
認証情報・ローカルパス・実行コードを含めない。

## implementation_notes

作成するファイルの内容:

```
# governance_template/.gitattributes
* text=auto eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.json text eol=lf
*.sh text eol=lf
```

## tests_or_checks

```bash
# .gitattributes が存在するか確認
test -f governance_template/.gitattributes && echo "OK" || echo "MISSING"

# 内容確認
cat governance_template/.gitattributes
```

## acceptance_criteria
- [ ] `governance_template/.gitattributes` が存在する
- [ ] `eol=lf` の設定が含まれる
- [ ] 他のファイルが変更されていない

## review_checklist
- 認証情報なし
- ローカルパスなし
- 追加ファイル以外の変更なし

## rollback_plan
`governance_template/.gitattributes` を削除してPRを閉じる。
