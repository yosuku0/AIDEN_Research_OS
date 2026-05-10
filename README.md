# AIDEN Research OS

AIDEN Research OS is a Personal AI Research Operating System. The operational name is AIDEN Research OS and the implementation name is base-ai-research-lab.

This repository is a research/control-plane scaffold. It is not a trading implementation, wallet, signer, deployment engine, or production-write agent.

## Architecture Overview

Human Final Approver -> Research Control Plane -> AIDEN Runtime -> Cloud AI, Local AI, GitHub Artifact Layer, Codex, and Market Labs -> Audit and Review -> Human Final Approver.

## Quick Start

1. Read SAFETY.md.
2. Read docs/system/PRODUCT_BOUNDARY.md.
3. Use docs/governance/SOURCE_OF_TRUTH.md before artifact promotion.
4. Start scoped work from codex/tasks.
5. Update research/ledgers for decisions, risks, approvals, incidents, and phase gates.

## Safety Constraints Summary

- Never give AIDEN, Cloud AI, Local AI, or Codex private keys, seeds, API keys, production credentials, or signing authority.
- Never implement deploy, approve, swap, bridge, transfer, or production write in any research sprint phase.
- Never connect research output directly to execution without a reviewed GitHub artifact and Human gate.
- Never use GitHub for raw prompts, raw transcripts, raw outputs, raw local logs, or secret backup.
- Never use a public Base endpoint as a production default.
- Never use Base-only branding for product identity.
- Never allow AI to auto-modify allowlists or risk limits.
- Never store credential values or local secret paths in GitHub.
- Never implement secret manager runtime, OS keychain adapter, or local encrypted vault before approval.
- Never add runtime code, CI changes, package installs, or provider integrations without explicit approval.

## Key Docs

- docs/system/SYSTEM_OF_SYSTEMS.md
- docs/system/EXECUTION_BOUNDARY.md
- docs/governance/APPROVAL_FLOW.md
- docs/governance/LEDGER_SCHEMA.md
- docs/security/HARDENING_POSTURE.md
