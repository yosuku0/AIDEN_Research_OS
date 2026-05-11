#!/usr/bin/env bash
set -euo pipefail

# Determine changed files against PR base (CI) or previous commit (local)
if [[ -n "${GITHUB_BASE_REF:-}" ]]; then
  git fetch --no-tags --depth=1 origin "${GITHUB_BASE_REF}" >/dev/null 2>&1 || true
  base_ref="origin/${GITHUB_BASE_REF}"
  changed_files=$(git diff --name-only "${base_ref}...HEAD")
else
  changed_files=$(git diff --name-only HEAD~1...HEAD 2>/dev/null || git diff --name-only)
fi

if [[ -z "${changed_files}" ]]; then
  echo "AUTO_EXECUTE_OK=true"
  echo "reason=no_changed_files"
  exit 0
fi

restricted=(
  ".github/CODEOWNERS"
  "SAFETY.md"
  "docs/system/PRODUCT_BOUNDARY.md"
  "AGENTS.md"
  "research/ledgers/approval-record.md"
  "research/ledgers/phase-gate-record.md"
)

human_required=false
while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  for r in "${restricted[@]}"; do
    if [[ "$file" == "$r" ]]; then
      human_required=true
      echo "restricted_change=$file"
    fi
  done
done <<< "$changed_files"

if [[ "$human_required" == true ]]; then
  echo "AUTO_EXECUTE_OK=false"
  echo "HUMAN_REVIEW_REQUIRED=true"
  echo "tier=2"
  exit 0
fi

echo "AUTO_EXECUTE_OK=true"
echo "HUMAN_REVIEW_REQUIRED=false"
echo "tier=0_or_1"
