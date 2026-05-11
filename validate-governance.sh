#!/usr/bin/env bash
# scripts/validate-governance.sh
#
# Local mirror of governance-ci.yml. Run before every commit.
# Exit 0 = all checks passed. Exit 1 = at least one failure.
#
# Usage:
#   bash scripts/validate-governance.sh          # all checks
#   bash scripts/validate-governance.sh --fast   # skip secret scan (faster)

set -euo pipefail

FAST_MODE=false
[[ "${1:-}" == "--fast" ]] && FAST_MODE=true

RED='\033[0;31m'
YEL='\033[1;33m'
GRN='\033[0;32m'
NC='\033[0m'

PASS=0
WARN=0
FAIL=0

pass() { echo -e "${GRN}  ✓ PASS${NC}  $1"; ((PASS++)); }
warn() { echo -e "${YEL}  ⚠ WARN${NC}  $1"; ((WARN++)); }
fail() { echo -e "${RED}  ✗ FAIL${NC}  $1"; ((FAIL++)); }

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AIDEN Research OS — Governance Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── CHECK 1: Required artifacts ──────────────────────────────────────────────
echo "▶ [1/6] Required artifact existence"

REQUIRED_FILES=(
  "README.md"
  "SAFETY.md"
  "AGENTS.md"
  "docs/system/PRODUCT_BOUNDARY.md"
  "docs/system/EXECUTION_BOUNDARY.md"
  "docs/system/SYSTEM_OF_SYSTEMS.md"
  "docs/governance/SOURCE_OF_TRUTH.md"
  "docs/governance/LEDGER_SCHEMA.md"
  "docs/governance/APPROVAL_FLOW.md"
  "docs/security/THREAT_MODEL.md"
  "docs/security/HARDENING_POSTURE.md"
  "research/ledgers/decision-log.md"
  "research/ledgers/approval-record.md"
  "research/ledgers/risk-ledger.md"
  "research/ledgers/phase-gate-record.md"
  "codex/templates/task-template.md"
)

for f in "${REQUIRED_FILES[@]}"; do
  if [ -f "$f" ]; then
    pass "$f"
  else
    fail "$f (missing)"
  fi
done

# ── CHECK 2: JSON validity ───────────────────────────────────────────────────
echo ""
echo "▶ [2/6] JSON file validity"

if ! command -v python3 &>/dev/null; then
  warn "python3 not found — skipping JSON validation"
else
  while IFS= read -r -d '' jsonfile; do
    if python3 -c "import json; json.load(open('$jsonfile'))" 2>/dev/null; then
      pass "$jsonfile"
    else
      fail "$jsonfile (invalid JSON)"
    fi
  done < <(find schemas/ fixtures/ -name '*.json' -print0 2>/dev/null)
fi

# ── CHECK 3: Schema validation with check-jsonschema ────────────────────────
echo ""
echo "▶ [3/6] Schema validation"

if ! command -v check-jsonschema &>/dev/null; then
  warn "check-jsonschema not installed (pip install check-jsonschema) — skipping"
else
  SCHEMA_FIXTURE_PAIRS=(
    "schemas/secret-manager/safe-config.schema.json:fixtures/security/secret-manager/no-secret.valid.json"
  )
  for pair in "${SCHEMA_FIXTURE_PAIRS[@]}"; do
    schema="${pair%%:*}"
    fixture="${pair##*:}"
    if [ ! -f "$schema" ] || [ ! -f "$fixture" ]; then
      warn "Skipping pair (file missing): $pair"
      continue
    fi
    if check-jsonschema --schemafile "$schema" "$fixture" &>/dev/null; then
      pass "$fixture validates against $schema"
    else
      fail "$fixture FAILS against $schema"
    fi
  done
fi

# ── CHECK 4: ADR required sections ──────────────────────────────────────────
echo ""
echo "▶ [4/6] ADR required sections"

REQUIRED_SECTIONS=("## Status" "## Context" "## Decision" "## Consequences")
ADR_FAIL=0

while IFS= read -r -d '' adr; do
  for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -q "^$section" "$adr" 2>/dev/null; then
      fail "$adr missing section: '$section'"
      ADR_FAIL=1
    fi
  done
  if [ "$ADR_FAIL" -eq 0 ]; then
    pass "$adr (all sections present)"
  fi
  ADR_FAIL=0
done < <(find docs/adr/ -name 'ADR-*.md' -print0 2>/dev/null)

# ── CHECK 5: Secret pattern scan ────────────────────────────────────────────
echo ""
echo "▶ [5/6] Secret pattern scan"

if $FAST_MODE; then
  warn "Skipped (--fast mode)"
else
  PATTERNS=(
    'sk-[a-zA-Z0-9]{20,}'
    'sk-proj-[a-zA-Z0-9_\-]{20,}'
    '0x[0-9a-fA-F]{64}'
    'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY'
    'AIza[0-9A-Za-z\-_]{35}'
    'password[:=][[:space:]]*["\x27][^"\x27]{8,}'
    'api[_-]?key[:=][[:space:]]*["\x27][^"\x27]{8,}'
  )

  SCAN_TARGETS=""
  for d in docs/ research/ fixtures/ schemas/; do
    [ -d "$d" ] && SCAN_TARGETS="$SCAN_TARGETS $d"
  done
  # Also scan packages if it exists (exclude .venv, __pycache__)
  [ -d "packages/" ] && SCAN_TARGETS="$SCAN_TARGETS packages/"

  SECRET_FOUND=false
  for pattern in "${PATTERNS[@]}"; do
    if matches=$(grep -rEn --exclude-dir='.venv' --exclude-dir='__pycache__' \
                   "$pattern" $SCAN_TARGETS 2>/dev/null); then
      echo "$matches" | while IFS= read -r line; do
        fail "Secret pattern [$pattern]: $line"
      done
      SECRET_FOUND=true
    fi
  done

  # Local path leakage
  if path_matches=$(grep -rEn \
    '(C:\\Users\\|C:\\\\Users\\\\|/home/[a-z]{2,}/|/Users/[A-Za-z]+/)' \
    docs/ research/ fixtures/ schemas/ 2>/dev/null); then
    echo "$path_matches" | while IFS= read -r line; do
      fail "Local path leak: $line"
    done
    SECRET_FOUND=true
  fi

  if ! $SECRET_FOUND; then
    pass "No secret-like patterns found in governed artifact paths"
  fi
fi

# ── CHECK 6: Forbidden files ─────────────────────────────────────────────────
echo ""
echo "▶ [6/6] Forbidden file check"

FORBIDDEN_PATTERNS=(
  ".env"
  ".env.*"
  "*.pem"
  "*.key"
  "*.p12"
  "*.pfx"
)

FORBIDDEN_FOUND=false
for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
  while IFS= read -r -d '' found; do
    fail "Forbidden file present: $found"
    FORBIDDEN_FOUND=true
  done < <(find . -name "$pattern" \
    -not -path './.git/*' \
    -not -path './.venv/*' \
    -not -path './packages/*/.venv/*' \
    -print0 2>/dev/null)
done

if ! $FORBIDDEN_FOUND; then
  pass "No forbidden files found"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  Results: ${GRN}$PASS passed${NC}  ${YEL}$WARN warnings${NC}  ${RED}$FAIL failed${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo -e "${RED}Governance validation FAILED. Fix all failures before committing.${NC}"
  exit 1
fi

if [ "$WARN" -gt 0 ]; then
  echo -e "${YEL}Governance validation passed with warnings. Review warnings above.${NC}"
  exit 0
fi

echo -e "${GRN}Governance validation PASSED.${NC}"
exit 0
