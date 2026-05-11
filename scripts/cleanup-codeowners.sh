#!/usr/bin/env bash
set -euo pipefail
if [ -f "CODEOWNERS" ] && [ -f ".github/CODEOWNERS" ]; then
    echo "Removing root CODEOWNERS (duplicate)"
    git rm "CODEOWNERS" 2>/dev/null || rm -f "CODEOWNERS"
else
    echo "No duplicate CODEOWNERS found"
fi