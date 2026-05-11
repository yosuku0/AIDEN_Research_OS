#!/usr/bin/env bash

set -euo pipefail

pass_count=0
warn_count=0
fail_count=0

pass() { printf 'PASS: %s\n' "$1"; pass_count=$((pass_count + 1)); }
warn() { printf 'WARN: %s\n' "$1"; warn_count=$((warn_count + 1)); }
fail() { printf 'FAIL: %s\n' "$1"; fail_count=$((fail_count + 1)); }

python_cmd() {
  if command -v python3 >/dev/null 2>&1; then printf 'python3'; return 0; fi
  if command -v python >/dev/null 2>&1; then printf 'python'; return 0; fi
  return 1
}

run_check_jsonschema() {
  if command -v check-jsonschema >/dev/null 2>&1; then
    check-jsonschema "$@"; return $?
  fi
  local py; if py=$(python_cmd); then "$py" -m check_jsonschema "$@"; return $?; fi
  return 127
}

json_syntax_ok() {
  local file="$1";
  local py; if py=$(python_cmd); then "$py" -m json.tool "$file" >/dev/null; return $?; fi
  perl -MJSON::PP -0777 -e 'decode_json(<>);' "$file" >/dev/null
}

check_artifact_existence() {
  printf '\n[1/5] Required artifact existence\n'
  local required=(
    README.md SAFETY.md docs/system/PRODUCT_BOUNDARY.md docs/system/SYSTEM_OF_SYSTEMS.md
    docs/governance/SOURCE_OF_TRUTH.md docs/governance/LEDGER_SCHEMA.md
    docs/governance/APPROVAL_FLOW.md docs/governance/SCHEMA_EVOLUTION_POLICY.md
    docs/governance/ADR_DIFFERENTIATION_GUIDE.md
    research/ledgers/decision-log.md research/ledgers/approval-record.md
    research/ledgers/incident-record.md research/ledgers/phase-gate-record.md
    codex/templates/task-template.md scripts/validate-governance.sh
  )
  local file; for file in "${required[@]}"; do
    if [[ -f "$file" ]]; then pass "$file"; else fail "$file is missing"; fi
  done
}

check_schema_validation() {
  printf '\n[2/5] Schema validation\n'
  local schema_validation_available=true
  if ! run_check_jsonschema --version >/dev/null 2>&1; then
    schema_validation_available=false
    warn "check-jsonschema unavailable; using JSON syntax checks only"
  fi

  local schema
  while IFS= read -r schema; do
    if [[ "$schema_validation_available" == true ]]; then
      if run_check_jsonschema --check-metaschema "$schema" >/dev/null; then pass "$schema metaschema"
      else fail "$schema failed metaschema validation"; fi
    elif json_syntax_ok "$schema"; then pass "$schema JSON syntax"
    else fail "$schema is not valid JSON"; fi
  done < <(find schemas -name '*.schema.json' -print 2>/dev/null | sort)

  local fixture
  while IFS= read -r fixture; do
    if json_syntax_ok "$fixture"; then pass "$fixture JSON syntax"
    else fail "$fixture is not valid JSON"; fi
  done < <(find fixtures -name '*.json' -print 2>/dev/null | sort)

  # Schema-fixture pair validation
  if [[ "$schema_validation_available" == true ]]; then
    printf '\n  --- Schema-Fixture Pair Validation ---\n'
    local sf_failed=0
    # Governance fixtures
    for schema_file in schemas/governance/*.schema.json; do
      local base=$(basename "$schema_file" .schema.json)
      if [[ -f "fixtures/governance/${base}.valid.json" ]]; then
        if run_check_jsonschema --schemafile "$schema_file" "fixtures/governance/${base}.valid.json" >/dev/null; then
          pass "governance/${base}.valid.json validates"
        else fail "governance/${base}.valid.json failed"; sf_failed=1; fi
      fi
      if [[ -f "fixtures/governance/${base}.invalid.json" ]]; then
        if run_check_jsonschema --schemafile "$schema_file" "fixtures/governance/${base}.invalid.json" >/dev/null; then
          fail "governance/${base}.invalid.json unexpectedly passed"; sf_failed=1
        else pass "governance/${base}.invalid.json correctly rejected"; fi
      fi
    done
    # Research-lab fixtures
    for schema_file in schemas/research-lab/*.schema.json; do
      local base=$(basename "$schema_file" .schema.json)
      if [[ -f "fixtures/research-lab/${base}.valid.json" ]]; then
        if run_check_jsonschema --schemafile "$schema_file" "fixtures/research-lab/${base}.valid.json" >/dev/null; then
          pass "research-lab/${base}.valid.json validates"
        else fail "research-lab/${base}.valid.json failed"; sf_failed=1; fi
      fi
      if [[ -f "fixtures/research-lab/${base}.invalid.json" ]]; then
        if run_check_jsonschema --schemafile "$schema_file" "fixtures/research-lab/${base}.invalid.json" >/dev/null; then
          fail "research-lab/${base}.invalid.json unexpectedly passed"; sf_failed=1
        else pass "research-lab/${base}.invalid.json correctly rejected"; fi
      fi
    done
    # Secret-manager fixtures
    if [[ -f schemas/secret-manager/safe-config.schema.json ]]; then
      local sm_fixture
      while IFS= read -r sm_fixture; do
        if [[ "$sm_fixture" == *.valid.json ]]; then
          if run_check_jsonschema --schemafile schemas/secret-manager/safe-config.schema.json "$sm_fixture" >/dev/null; then
            pass "secret-manager/$(basename "$sm_fixture") validates"
          else fail "secret-manager/$(basename "$sm_fixture") failed"; sf_failed=1; fi
        fi
      done < <(find fixtures/security/secret-manager -name '*.json' -print 2>/dev/null | sort)
      if [[ -f fixtures/security/secret-manager/forbidden-content.cases.json ]]; then
        if run_check_jsonschema --schemafile schemas/secret-manager/safe-config.schema.json \
          fixtures/security/secret-manager/forbidden-content.cases.json >/dev/null; then
          fail "forbidden-content.cases.json unexpectedly passed"; sf_failed=1
        else pass "forbidden-content.cases.json correctly rejected"; fi
      fi
    fi
    if [[ "$sf_failed" -eq 1 ]]; then fail "Some schema-fixture pairs failed"; fi
  fi
}

check_ledger_structure() {
  printf '\n[3/5] Ledger structure validation\n'
  if [[ -f research/ledgers/approval-record.md ]]; then
    if grep -q "approval_criteria_met" research/ledgers/approval-record.md; then
      pass "approval-record.md has approval_criteria_met"
    else fail "approval-record.md missing approval_criteria_met"; fi
    local ar_count=$(grep -Ec '^\| AR-[0-9]+' research/ledgers/approval-record.md || true)
    echo "  $ar_count AR entries found"
  fi
  if [[ -f research/ledgers/decision-log.md ]]; then
    local dl_count=$(grep -Ec '^\| DL-[0-9]+' research/ledgers/decision-log.md || true)
    echo "  $dl_count decision entries found"
    pass "decision-log.md structure OK"
  fi
  if [[ -f research/ledgers/incident-record.md ]]; then
    local resolved=$(grep -c "status.*resolved" research/ledgers/incident-record.md || true)
    echo "  $resolved resolved incidents"
    pass "incident-record.md structure OK"
  fi
}

check_secret_scan() {
  printf '\n[4/5] Secret pattern scan\n'
  local scan_paths=()
  local path
  for path in docs research schemas fixtures tests packages scripts; do
    [[ -e "$path" ]] && scan_paths+=("$path")
  done
  local patterns=(
    'sk-[A-Za-z0-9]{20,}' 'sk-proj-[A-Za-z0-9_-]{20,}'
    'ghp_[A-Za-z0-9]{36}' 'AIza[0-9A-Za-z_-]{35}'
    '0x[0-9a-fA-F]{40,}'
    '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'
  )
  local found=false
  for pattern in "${patterns[@]}"; do
    local matches
    matches=$(grep -RInE --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ \
      -- "$pattern" "${scan_paths[@]}" 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
      fail "pattern detected: $pattern"
      echo "$matches" | cut -d: -f1 | sort -u | sed 's/^/  file: /'
      found=true
    fi
  done
  local env_matches
  env_matches=$(find . -path './.git' -prune -o \( -name '.env' -o -name '.env.*' \) -print 2>/dev/null || true)
  if [[ -n "$env_matches" ]]; then fail "environment file detected"; echo "$env_matches"; found=true; fi
  if [[ "$found" == false ]]; then pass "no secret-like patterns found"; fi
  rm -f /tmp/aiden-secret-scan.txt 2>/dev/null || true
}

check_approval_status() {
  printf '\n[5/5] Approval status check\n'
  local approval_file=research/ledgers/approval-record.md
  if [[ ! -f "$approval_file" ]]; then warn "$approval_file missing"; return; fi
  local total=$(grep -Ec '^\| AR-[0-9]+' "$approval_file" || true)
  local pending=$(grep -Ec '^\| AR-[0-9]+.*\|[[:space:]]*pending[[:space:]]*\|' "$approval_file" || true)
  local approved=$(grep -Ec '^\| AR-[0-9]+.*\|[[:space:]]*approve[[:space:]]*\|' "$approval_file" || true)
  if [[ "$total" -gt 0 && "$total" -eq "$pending" ]]; then
    warn "all $total ARs pending; Human approval required"
  elif [[ "$approved" -gt 0 ]]; then
    pass "$approved approved, $pending pending of $total ARs"
  else pass "$total ARs checked"; fi
}

# Run all checks
check_artifact_existence
check_schema_validation
check_ledger_structure
check_secret_scan
check_approval_status

printf '\n========================================\n'
printf 'Summary: %s passed, %s warnings, %s failed\n' "$pass_count" "$warn_count" "$fail_count"
printf '========================================\n'

if [[ "$fail_count" -gt 0 ]]; then exit 1; fi
