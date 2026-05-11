# GT-0002: governance_template — CODEOWNERS と governance-ci.yml の追加

## task_id
GT-0002-codeowners-ci

## title
governance_template に CODEOWNERS と Governance CI ワークフローを追加する

## status
draft

## human_approval_required
true

## task_class
governance

## risk_level
Medium

## goal
governance_template には CI も CODEOWNERS も存在しない。
これにより Fork した全プロジェクトが最初からゼロ保護で起動している。
CODEOWNERS テンプレートと governance-ci.yml を追加し、
テンプレートとしての最低限の保護基盤を提供する。

## background
監査レポート CRITICAL-T1（CI 不在）・CRITICAL-T2（CODEOWNERS 不在）の対応。
AIDEN Research OS 側で実装済みの CI をテンプレートに還元する。

## inputs
- 監査レポート CRITICAL-T1 / CRITICAL-T2 の修正パッチ
- aiden_research_os/governance-ci.yml（参照元）
- governance_template/ ディレクトリ（同プロジェクト内）

## in_scope
- `governance_template/.github/CODEOWNERS` の新規追加
- `governance_template/.github/workflows/governance-ci.yml` の新規追加

## out_of_scope
- ブランチ保護ルールの有効化（GitHub Settings での作業 — Human が行う）
- PLACEHOLDER_OWNER の実アカウント解決（Human が行う）
- スキーマ・ドキュメントの修正

## allowed_files
governance_template/.github/CODEOWNERS
governance_template/.github/workflows/governance-ci.yml

## forbidden_files
governance_template/src/**
governance_template/runtime/**
governance_template/.env
governance_template/.env.*
governance_template/schemas/**
governance_template/docs/**
governance_template/research/**

## required_outputs
- governance_template/.github/CODEOWNERS（新規）
- governance_template/.github/workflows/governance-ci.yml（新規）

## prohibited_work
PLACEHOLDER_OWNER を実アカウントに書き換えない（Human が行う）。
ブランチ保護を自動で有効化しない。
認証情報・ローカルパス・実行コードを含めない。

## implementation_notes

### governance_template/.github/CODEOWNERS

```
# Replace PLACEHOLDER_OWNER with your GitHub username
# Enable: Settings → Branches → main → Require review from Code Owners
* @PLACEHOLDER_OWNER
/docs/ @PLACEHOLDER_OWNER
/schemas/ @PLACEHOLDER_OWNER
/research/ @PLACEHOLDER_OWNER
/codex/ @PLACEHOLDER_OWNER
/SAFETY_TEMPLATE.md @PLACEHOLDER_OWNER
/README.md @PLACEHOLDER_OWNER
/AGENTS.md @PLACEHOLDER_OWNER
```

### governance_template/.github/workflows/governance-ci.yml

```yaml
name: Governance CI

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  artifact-existence:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate required template artifacts exist
        shell: bash
        run: |
          required=(
            README.md
            SAFETY_TEMPLATE.md
            docs/governance/SOURCE_OF_TRUTH.md
            docs/governance/APPROVAL_FLOW.md
            research/ledgers/decision-log.md
            codex/templates/task-template.md
            AGENTS.md
          )
          failed=0
          for file in "${required[@]}"; do
            test -f "$file" \
              && echo "OK: $file" \
              || { echo "MISSING: $file"; failed=1; }
          done
          exit $failed

  content-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan for secret-like patterns
        shell: bash
        run: |
          if grep -rEI \
            "(PRIVATE_KEY|ghp_[A-Za-z0-9]{36}|sk-[A-Za-z0-9]{48}|AIza[0-9A-Za-z_-]{35})" \
            docs/ research/ schemas/ \
            --include="*.md" --include="*.json" 2>/dev/null; then
            echo "ERROR: secret-like pattern detected"
            exit 1
          fi
          echo "OK: no secret-like patterns"

      - name: Scan for unresolved placeholders
        shell: bash
        run: |
          if grep -rI \
            "replace before use\|PLACEHOLDER_OWNER\|placeholder scope" \
            docs/ research/ codex/ \
            --include="*.md" 2>/dev/null; then
            echo "ERROR: unresolved placeholder found"
            exit 1
          fi
          echo "OK: no unresolved placeholders"

      - name: Verify forbidden files are absent
        shell: bash
        run: |
          failed=0
          for name in package.json package-lock.json yarn.lock \
                      pnpm-lock.yaml Dockerfile docker-compose.yml; do
            found=$(find . -path "./.git" -prune -o \
                    -name "$name" -print | grep -v "^./.git" || true)
            if [ -n "$found" ]; then
              echo "ERROR: forbidden file found: $found"
              failed=1
            fi
          done
          exit $failed

  schema-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate JSON schema structure
        shell: bash
        run: |
          python3 << 'EOF'
          import json, glob, sys
          errors = []
          for f in glob.glob('schemas/**/*.json', recursive=True):
              try:
                  s = json.load(open(f))
                  if s.get('additionalProperties') != False:
                      errors.append(f'FAIL [{f}]: additionalProperties must be false')
                  else:
                      print(f'OK: {f}')
              except Exception as e:
                  errors.append(f'FAIL [{f}]: {e}')
          for e in errors:
              print(e)
          sys.exit(1 if [e for e in errors if e.startswith('FAIL')] else 0)
          EOF
```

## tests_or_checks

```bash
# ファイル存在確認
test -f governance_template/.github/CODEOWNERS \
  && echo "OK: CODEOWNERS" || echo "MISSING"
test -f governance_template/.github/workflows/governance-ci.yml \
  && echo "OK: CI" || echo "MISSING"

# CODEOWNERS に PLACEHOLDER_OWNER が含まれるか確認
grep -q "PLACEHOLDER_OWNER" governance_template/.github/CODEOWNERS \
  && echo "OK: placeholder present" || echo "ERROR: placeholder missing"

# YAML 構文チェック（python3）
python3 -c "
import yaml, sys
try:
    yaml.safe_load(open('governance_template/.github/workflows/governance-ci.yml'))
    print('OK: valid YAML')
except yaml.YAMLError as e:
    print(f'FAIL: {e}')
    sys.exit(1)
"
```

## acceptance_criteria
- [ ] `governance_template/.github/CODEOWNERS` が存在する
- [ ] `governance_template/.github/workflows/governance-ci.yml` が存在する
- [ ] CODEOWNERS に `PLACEHOLDER_OWNER` の記述がある
- [ ] CI YAML が構文的に正しい
- [ ] 他のファイルが変更されていない

## review_checklist
- PLACEHOLDER_OWNER が実アカウントに書き換えられていないこと
- CI が `workflow_dispatch` トリガーを持つこと
- 認証情報・ローカルパスなし

## rollback_plan
追加した2ファイルを削除してPRを閉じる。
