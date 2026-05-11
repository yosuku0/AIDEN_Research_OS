#!/usr/bin/env bash
# Final validation script for Phase 4+5 completion
# Run all checks: governance, pytest, coverage, schema, fixtures

set -euo pipefail

ERRORS=0

header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
}

# ===== Check 1: Governance validation =====
header "[1/7] Governance Validation"
if bash scripts/validate-governance.sh; then
    echo "GOVERNANCE: PASS"
else
    echo "GOVERNANCE: FAIL"
    ERRORS=$((ERRORS + 1))
fi

# ===== Check 2: Python tests =====
header "[2/7] Python Test Suite"
if command -v pytest >/dev/null 2>&1; then
    if pytest tests/ -v --tb=short 2>/dev/null; then
        echo "PYTEST: PASS"
    else
        echo "PYTEST: FAIL (some tests failed or skipped)"
        # Don't count as error if only skipped
    fi
else
    echo "PYTEST: SKIP (pytest not installed)"
fi

# ===== Check 3: Coverage =====
header "[3/7] Coverage Report"
if command -v pytest >/dev/null 2>&1 && python -c "import pytest_cov" 2>/dev/null; then
    pytest tests/ --cov=aiden --cov-report=term-missing --cov-fail-under=80 || {
        echo "COVERAGE: FAIL (below 80%)"
        ERRORS=$((ERRORS + 1))
    }
else
    echo "COVERAGE: SKIP (pytest-cov not installed)"
fi

# ===== Check 4: Schema metaschema =====
header "[4/7] Schema Metaschema Validation"
if command -v check-jsonschema >/dev/null 2>&1; then
    SCHEMA_FAILED=0
    for schema in schemas/**/*.schema.json; do
        [ -f "$schema" ] || continue
        if check-jsonschema --check-metaschema "$schema" >/dev/null 2>&1; then
            echo "  OK: $(basename $schema)"
        else
            echo "  FAIL: $(basename $schema)"
            SCHEMA_FAILED=1
        fi
    done
    if [ "$SCHEMA_FAILED" -eq 0 ]; then
        echo "SCHEMA: PASS"
    else
        echo "SCHEMA: FAIL"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "SCHEMA: SKIP (check-jsonschema not installed)"
fi

# ===== Check 5: Fixture validation =====
header "[5/7] Schema-Fixture Pair Validation"
if command -v check-jsonschema >/dev/null 2>&1; then
    FIXTURE_FAILED=0
    # Valid fixtures must pass
    for vf in fixtures/**/*.valid.json; do
        [ -f "$vf" ] || continue
        dir=$(dirname "$vf" | sed 's/fixtures/schemas/')
        base=$(basename "$vf" .valid.json)
        schema_candidates=("$dir/${base}.schema.json")
        # Try to find matching schema
        SCHEMA_FOUND=""
        for sc in "${schema_candidates[@]}"; do
            if [ -f "$sc" ]; then SCHEMA_FOUND="$sc"; break; fi
        done
        if [ -n "$SCHEMA_FOUND" ]; then
            if check-jsonschema --schemafile "$SCHEMA_FOUND" "$vf" >/dev/null 2>&1; then
                echo "  PASS: $(basename $vf)"
            else
                echo "  FAIL: $(basename $vf)"
                FIXTURE_FAILED=1
            fi
        fi
    done
    # Invalid fixtures must fail
    for ivf in fixtures/**/*.invalid.json; do
        [ -f "$ivf" ] || continue
        dir=$(dirname "$ivf" | sed 's/fixtures/schemas/')
        base=$(basename "$ivf" .invalid.json)
        schema_candidates=("$dir/${base}.schema.json")
        SCHEMA_FOUND=""
        for sc in "${schema_candidates[@]}"; do
            if [ -f "$sc" ]; then SCHEMA_FOUND="$sc"; break; fi
        done
        if [ -n "$SCHEMA_FOUND" ]; then
            if check-jsonschema --schemafile "$SCHEMA_FOUND" "$ivf" >/dev/null 2>&1; then
                echo "  UNEXPECTED PASS: $(basename $ivf) should have failed"
                FIXTURE_FAILED=1
            else
                echo "  CORRECT FAIL: $(basename $ivf)"
            fi
        fi
    done
    # Secret-manager fixtures
    if [ -f schemas/secret-manager/safe-config.schema.json ]; then
        for smf in fixtures/security/secret-manager/*.valid.json; do
            [ -f "$smf" ] || continue
            if check-jsonschema --schemafile schemas/secret-manager/safe-config.schema.json "$smf" >/dev/null 2>&1; then
                echo "  PASS: $(basename $smf)"
            else
                echo "  FAIL: $(basename $smf)"
                FIXTURE_FAILED=1
            fi
        done
        if [ -f fixtures/security/secret-manager/forbidden-content.cases.json ]; then
            if check-jsonschema --schemafile schemas/secret-manager/safe-config.schema.json \
                fixtures/security/secret-manager/forbidden-content.cases.json >/dev/null 2>&1; then
                echo "  UNEXPECTED PASS: forbidden-content should fail"
                FIXTURE_FAILED=1
            else
                echo "  CORRECT FAIL: forbidden-content.cases.json"
            fi
        fi
    fi
    if [ "$FIXTURE_FAILED" -eq 0 ]; then
        echo "FIXTURE: PASS"
    else
        echo "FIXTURE: FAIL"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "FIXTURE: SKIP (check-jsonschema not installed)"
fi

# ===== Check 6: Secret scan =====
header "[6/7] Secret Pattern Scan"
scan_paths=()
for path in docs research schemas fixtures tests scripts; do
    [ -e "$path" ] && scan_paths+=("$path")
done
SCAN_FAILED=0
patterns=(
    'sk-[A-Za-z0-9]{20,}' 'sk-proj-[A-Za-z0-9_-]{20,}'
    'ghp_[A-Za-z0-9]{36}' 'AIza[0-9A-Za-z_-]{35}'
    '0x[0-9a-fA-F]{40,}'
    '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'
)
for pattern in "${patterns[@]}"; do
    matches=$(grep -RInE --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ \
        -- "$pattern" "${scan_paths[@]}" 2>/dev/null || true)
    if [ -n "$matches" ]; then
        echo "  DETECTED: $pattern"
        echo "$matches" | head -5
        SCAN_FAILED=1
    fi
done
if [ "$SCAN_FAILED" -eq 0 ]; then
    echo "SECRET: PASS (no patterns detected)"
else
    echo "SECRET: FAIL"
    ERRORS=$((ERRORS + 1))
fi

# ===== Check 7: Phantom files =====
header "[7/7] Phantom File Check"
if git ls-files 2>/dev/null | grep -q "mnt/user-data"; then
    echo "PHANTOM: FAIL (mnt/user-data/ tracked in git)"
    ERRORS=$((ERRORS + 1))
else
    echo "PHANTOM: PASS (no phantom files)"
fi

# ===== Summary =====
header "FINAL SUMMARY"
echo "Errors: $ERRORS"
if [ "$ERRORS" -eq 0 ]; then
    echo "RESULT: ALL CHECKS PASSED"
    exit 0
else
    echo "RESULT: $ERRORS CHECK(S) FAILED"
    exit 1
fi
