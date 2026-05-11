# GT-0003: governance_template — 3スキーマの修正

## task_id
GT-0003-schema-fixes

## title
governance_template の JSON Schema 3ファイルを修正する（minLength / 型修正 / フィールド追加）

## status
draft

## human_approval_required
false

## task_class
governance

## risk_level
Medium

## goal
以下の3つのスキーマ問題を修正する:
1. 全スキーマの required 文字列フィールドに `minLength: 1` を追加（空文字列防止）
2. `risk-ledger.schema.json` の `mitigation_controls` を `string` → `array` に修正
3. `approval-record.schema.json` に `linked_phase_gate` フィールドを追加
4. `decision-log.schema.json` に `alternatives`・`consequences` フィールドを追加

## background
監査レポート HIGH-T2（minLength欠落）・HIGH-T3（mitigation_controls型誤り）・
MEDIUM-T2（linked_phase_gate欠落）・MEDIUM-T3（alternatives/consequences欠落）の対応。
AIDEN Research OS 側では既にこれらの修正が適用されており、
今回はテンプレート側に還元する。

## inputs
- 監査レポートの HIGH-T2 / HIGH-T3 / MEDIUM-T2 / MEDIUM-T3 項目
- governance_template/schemas/governance/ 配下の3ファイル

## in_scope
- `governance_template/schemas/governance/approval-record.schema.json` の修正
- `governance_template/schemas/governance/decision-log.schema.json` の修正
- `governance_template/schemas/governance/risk-ledger.schema.json` の修正

## out_of_scope
- `required` 配列への新フィールド追加（破壊的変更のため禁止）
- Markdown台帳ファイルの変更
- CI・ドキュメントの変更

## allowed_files
governance_template/schemas/governance/approval-record.schema.json
governance_template/schemas/governance/decision-log.schema.json
governance_template/schemas/governance/risk-ledger.schema.json

## forbidden_files
governance_template/research/**
governance_template/docs/**
governance_template/codex/**
governance_template/.github/**
governance_template/README.md
governance_template/SAFETY_TEMPLATE.md

## required_outputs
- approval-record.schema.json（minLength追加 + linked_phase_gate追加）
- decision-log.schema.json（minLength追加 + alternatives/consequences追加）
- risk-ledger.schema.json（minLength追加 + mitigation_controls を array に修正）

## prohibited_work
`required` 配列に新フィールドを追加しない（既存データとの後方互換を壊す）。
`additionalProperties: false` を削除しない。
`enum` の既存値を削除しない。

## implementation_notes

### approval-record.schema.json（完全な修正版）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "id",
    "approval_type",
    "requested_by",
    "approver",
    "approval_scope",
    "decision"
  ],
  "properties": {
    "id": { "type": "string", "minLength": 1 },
    "approval_type": { "type": "string", "minLength": 1 },
    "requested_by": { "type": "string", "minLength": 1 },
    "approver": { "type": "string", "minLength": 1 },
    "approval_scope": { "type": "string", "minLength": 1 },
    "linked_pr": { "type": "string" },
    "linked_phase_gate": { "type": "string" },
    "decision": {
      "enum": ["approve", "edit", "reject", "hold", "pending"]
    },
    "conditions": { "type": "string" },
    "timestamp": { "type": "string" }
  }
}
```

### decision-log.schema.json（完全な修正版）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "id",
    "decision_type",
    "status",
    "owner",
    "decision",
    "rationale",
    "rollback_plan"
  ],
  "properties": {
    "id": { "type": "string", "minLength": 1 },
    "decision_type": { "type": "string", "minLength": 1 },
    "status": { "type": "string", "minLength": 1 },
    "owner": { "type": "string", "minLength": 1 },
    "linked_adr": { "type": "string" },
    "linked_codex_task": { "type": "string" },
    "decision": { "type": "string", "minLength": 1 },
    "alternatives": {
      "type": "array",
      "items": { "type": "string" }
    },
    "rationale": { "type": "string", "minLength": 1 },
    "consequences": { "type": "string" },
    "rollback_plan": { "type": "string", "minLength": 1 }
  }
}
```

### risk-ledger.schema.json（完全な修正版）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "id",
    "risk_class",
    "severity",
    "likelihood",
    "status",
    "trigger",
    "mitigation_controls",
    "detection_method",
    "residual_risk"
  ],
  "properties": {
    "id": { "type": "string", "minLength": 1 },
    "risk_class": { "type": "string", "minLength": 1 },
    "severity": { "enum": ["low", "medium", "high", "critical"] },
    "likelihood": { "enum": ["low", "medium", "high"] },
    "status": { "type": "string", "minLength": 1 },
    "trigger": { "type": "string", "minLength": 1 },
    "mitigation_controls": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 },
      "minItems": 1
    },
    "detection_method": { "type": "string", "minLength": 1 },
    "residual_risk": { "type": "string", "minLength": 1 }
  }
}
```

## tests_or_checks

```bash
python3 << 'EOF'
import json, glob, sys

errors = []
for f in glob.glob('governance_template/schemas/**/*.json', recursive=True):
    s = json.load(open(f))

    # additionalProperties check
    if s.get('additionalProperties') != False:
        errors.append(f'FAIL [{f}]: additionalProperties must be false')
        continue

    # minLength check on required string fields
    for field in s.get('required', []):
        prop = s['properties'].get(field, {})
        if prop.get('type') == 'string' \
           and 'minLength' not in prop \
           and 'enum' not in prop:
            errors.append(f'WARN [{f}]: required field "{field}" lacks minLength')

    # mitigation_controls type check
    mc = s.get('properties', {}).get('mitigation_controls', {})
    if mc and mc.get('type') == 'string':
        errors.append(f'FAIL [{f}]: mitigation_controls must be array, not string')

    print(f'OK: {f}')

for e in errors: print(e)
sys.exit(1 if [e for e in errors if e.startswith('FAIL')] else 0)
EOF
```

## acceptance_criteria
- [ ] 3スキーマ全ての `additionalProperties: false` が維持されている
- [ ] required な string フィールド全てに `minLength: 1` がある
- [ ] `risk-ledger.schema.json` の `mitigation_controls` が `array` 型になっている
- [ ] `approval-record.schema.json` に `linked_phase_gate` フィールドがある
- [ ] `decision-log.schema.json` に `alternatives`・`consequences` フィールドがある
- [ ] `required` 配列に新フィールドが追加されていない
- [ ] python3 バリデーションスクリプトがパスする

## review_checklist
- `required` への破壊的追加なし
- `additionalProperties: false` 維持
- `enum` 値の削除なし
- Markdown台帳ファイルの変更なし

## rollback_plan
3ファイルを Git で revert してPRを閉じる。
台帳への影響なし（スキーマ変更はMarkdown台帳を直接変更しないため）。
