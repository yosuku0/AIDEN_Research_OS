#!/usr/bin/env bash
set -euo pipefail
ROOT_SCHEMA="phase-gate-record.schema.json"
GOV_SCHEMA="schemas/governance/phase-gate-record.schema.json"
if [ -f "$ROOT_SCHEMA" ]; then
    if [ -f "$GOV_SCHEMA" ]; then
        echo "Root $ROOT_SCHEMA is duplicate - removing"
        git rm "$ROOT_SCHEMA" 2>/dev/null || rm -f "$ROOT_SCHEMA"
    else
        echo "Moving $ROOT_SCHEMA to $GOV_SCHEMA"
        mv "$ROOT_SCHEMA" "$GOV_SCHEMA"
        git add "$GOV_SCHEMA"
    fi
else
    echo "No root-level schema to clean up"
fi