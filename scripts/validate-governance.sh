#!/usr/bin/env bash

set -euo pipefail

pass_count=0
warn_count=0
fail_count=0

pass() {
  printf 'PASS: %s\n' "$1"
  pass_count=$((pass_count + 1))
}

warn() {
  printf 'WARN: %s\n' "$1"
  warn_count=$((warn_count + 1))
}

fail() {
  printf 'FAIL: %s\n' "$1"
  fail_count=$((fail_count + 1))
}

python_cmd() {
  if command -v python3 >/dev/null 2>&1; then
    printf 'python3'
    return 0
  fi

  if command -v python >/dev/null 2>&1; then
    printf 'python'
    return 0
  fi

  return 1
}

run_check_jsonschema() {
  if command -v check-jsonschema >/dev/null 2>&1; then
    check-jsonschema "$@"
    return $?
  fi

  local py
  if py=$(python_cmd); then
    "$py" -m check_jsonschema "$@"
    return $?
  fi

  return 127
}

json_syntax_ok() {
  local file="$1"
  local py

  if py=$(python_cmd); then
    "$py" -m json.tool "$file" >/dev/null
    return $?
  fi

  perl -MJSON::PP -0777 -e 'decode_json(<>);' "$file" >/dev/null
}

check_artifact_existence() {
  printf '\n[1/4] Required artifact existence\n'

  local required=(
    README.md
    SAFETY.md
    docs/system/PRODUCT_BOUNDARY.md
    docs/system/SYSTEM_OF_SYSTEMS.md
    docs/governance/SOURCE_OF_TRUTH.md
    docs/governance/LEDGER_SCHEMA.md
    docs/governance/APPROVAL_FLOW.md
    research/ledgers/decision-log.md
    research/ledgers/approval-record.md
    codex/templates/task-template.md
    scripts/validate-governance.sh
  )

  local file
  for file in "${required[@]}"; do
    if [[ -f "$file" ]]; then
      pass "$file"
    else
      fail "$file is missing"
    fi
  done
}

check_schema_validation() {
  printf '\n[2/4] Schema validation\n'

  local schema_validation_available=true
  if ! run_check_jsonschema --version >/dev/null 2>&1; then
    schema_validation_available=false
    warn "check-jsonschema is unavailable in this shell; falling back to JSON syntax checks"
  fi

  local schema
  while IFS= read -r schema; do
    if [[ "$schema_validation_available" == true ]]; then
      if run_check_jsonschema --check-metaschema "$schema" >/dev/null; then
        pass "$schema"
      else
        fail "$schema failed metaschema validation"
      fi
    elif json_syntax_ok "$schema"; then
      pass "$schema JSON syntax"
    else
      fail "$schema is not valid JSON"
    fi
  done < <(find schemas -name '*.json' -print 2>/dev/null | sort)

  local fixture
  while IFS= read -r fixture; do
    if json_syntax_ok "$fixture"; then
      pass "$fixture"
    else
      fail "$fixture is not valid JSON"
    fi
  done < <(find fixtures -name '*.json' -print 2>/dev/null | sort)

  if [[ "$schema_validation_available" == true && -f schemas/secret-manager/safe-config.schema.json && -f fixtures/security/secret-manager/no-secret.valid.json ]]; then
    if run_check_jsonschema \
      --schemafile schemas/secret-manager/safe-config.schema.json \
      fixtures/security/secret-manager/no-secret.valid.json >/dev/null; then
      pass "safe config fixture validates against safe-config schema"
    else
      fail "safe config fixture failed safe-config schema validation"
    fi
  elif [[ "$schema_validation_available" == false ]]; then
    warn "safe config fixture schema validation skipped because check-jsonschema is unavailable"
  else
    warn "safe config schema or fixture missing; skipped pair validation"
  fi
}

check_secret_scan() {
  printf '\n[3/4] Secret pattern scan\n'

  local scan_paths=()
  local path
  for path in docs research schemas fixtures tests packages scripts; do
    if [[ -e "$path" ]]; then
      scan_paths+=("$path")
    fi
  done

  local patterns=(
    'sk-[A-Za-z0-9]{20,}'
    'sk-proj-[A-Za-z0-9_-]{20,}'
    'ghp_[A-Za-z0-9]{36}'
    'AIza[0-9A-Za-z_-]{35}'
    '0x[0-9a-fA-F]{40,}'
    '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'
    'password[[:space:]]*[:=][[:space:]]*["'\''][^"'\'']{8,}["'\'']'
    'api[_-]?key[[:space:]]*[:=][[:space:]]*["'\''][^"'\'']{8,}["'\'']'
  )

  local found=false
  local pattern
  for pattern in "${patterns[@]}"; do
    local matches
    matches=$(grep -RInE --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ -- "$pattern" "${scan_paths[@]}" 2>/dev/null || true)
    if [[ -n "$matches" ]]; then
      fail "secret-like pattern detected in governed file"
      # SECURITY FIX: Output file paths only (first field), not the matched content
      # This prevents secret candidates from leaking into logs or temp files
      echo "$matches" | cut -d: -f1 | sort -u | sed 's/^/  file: /'
      found=true
    fi
  done

  local env_matches
  env_matches=$(find . -path './.git' -prune -o \( -name '.env' -o -name '.env.*' \) -print 2>/dev/null || true)
  if [[ -n "$env_matches" ]]; then
    fail "environment file detected"
    printf '%s\n' "$env_matches" | sed 's/^/  /'
    found=true
  fi

  if [[ "$found" == false ]]; then
    pass "no secret-like patterns found"
  fi

}

check_approval_status() {
  printf '\n[4/4] Approval status check\n'

  local approval_file=research/ledgers/approval-record.md
  if [[ ! -f "$approval_file" ]]; then
    warn "$approval_file is missing"
    return
  fi

  local total pending approved
  total=$(grep -Ec '^\| AR-[0-9]+' "$approval_file" || true)
  pending=$(grep -Ec '^\| AR-[0-9]+.*\|[[:space:]]*pending[[:space:]]*\|' "$approval_file" || true)
  approved=$(grep -Ec '^\| AR-[0-9]+.*\|[[:space:]]*approve[[:space:]]*\|' "$approval_file" || true)

  if [[ "$total" -gt 0 && "$total" -eq "$pending" ]]; then
    warn "all $total approval records remain pending; human approval is required before merge"
  elif [[ "$approved" -gt 0 ]]; then
    pass "approval records checked: $approved approved, $pending pending of $total total"
  else
    pass "approval records checked: $pending of $total records pending"
  fi

  if grep -q "approval_criteria_met" "$approval_file"; then
    pass "approval_criteria_met field is present"
  else
    fail "approval_criteria_met field is missing"
  fi
}

# Run all checks
check_artifact_existence
check_schema_validation
check_secret_scan
check_approval_status

printf '\nSummary: %s passed, %s warnings, %s failed\n' "$pass_count" "$warn_count" "$fail_count"

if [[ "$fail_count" -gt 0 ]]; then
  exit 1
fi
