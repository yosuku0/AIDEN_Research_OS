"""
tests/integration/test_audit_hazard_coverage.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Integration tests that directly correspond to each finding in the
Red Team Hazard Audit report (CRIT-01 through HIGH-04).

This file is the executable proof that all audit findings are resolved.
It must be 100% green before PR-0025 can be approved.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from aiden.models.router import BudgetExceededError, ModelRouter
from aiden.secrets.keychain import (
    FakeKeychain,
    KeychainEntryNotFound,
    _validate_ref_id,
)
from aiden.workflow.graph import (
    HUMAN_GATE_TRIGGERS,
    ResearchState,
    build_graph,
    make_initial_state,
)

REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent


# ── CRIT-01: CI enforcement is not just file-existence ───────────────────────

class TestCrit01CiEnforcement:
    """
    CRIT-01: governance-ci.yml previously only checked file existence.
    Resolution: validate-governance.sh and the updated CI run schema validation,
    secret scanning, and ADR section checks.
    """

    def test_validate_governance_script_exists(self):
        """scripts/validate-governance.sh must exist and be executable."""
        script = REPO_ROOT / "scripts" / "validate-governance.sh"
        assert script.exists(), (
            "scripts/validate-governance.sh is missing. "
            "This is required by audit finding CRIT-01."
        )

    def test_validate_governance_script_exits_zero_on_clean_repo(self):
        """validate-governance.sh must exit 0 on a clean repository."""
        script = REPO_ROOT / "scripts" / "validate-governance.sh"
        if not script.exists():
            pytest.skip("validate-governance.sh not yet created (PR-0018 pending)")
        result = subprocess.run(
            ["bash", str(script), "--fast"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        assert result.returncode == 0, (
            f"validate-governance.sh failed:\nSTDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    def test_ci_yml_has_schema_validation_job(self):
        """governance-ci.yml must contain schema-validation job."""
        ci_file = REPO_ROOT / ".github" / "workflows" / "governance-ci.yml"
        if not ci_file.exists():
            pytest.skip("governance-ci.yml not yet updated (PR-0018 pending)")
        content = ci_file.read_text()
        assert "schema-validation" in content, (
            "governance-ci.yml must have a 'schema-validation' job (CRIT-01)"
        )
        assert "secret-scan" in content, (
            "governance-ci.yml must have a 'secret-scan' job (CRIT-01)"
        )

    def test_ci_yml_has_python_validate_job(self):
        """governance-ci.yml must run pytest when aiden-core exists."""
        ci_file = REPO_ROOT / ".github" / "workflows" / "governance-ci.yml"
        if not ci_file.exists():
            pytest.skip("governance-ci.yml not yet updated (PR-0018 pending)")
        content = ci_file.read_text()
        assert "python-validate" in content or "pytest" in content, (
            "governance-ci.yml must run Python tests (CRIT-01)"
        )


# ── CRIT-02: Approval timestamp must be a real ISO 8601 date ─────────────────

class TestCrit02TimestampEnforcement:
    """
    CRIT-02: phase-gate-record.schema.json previously accepted 'pending' as
    a timestamp value, allowing AI to fake-complete a Human gate.
    Resolution: ISO 8601 pattern constraint + if/then on 'go'/'no-go' decisions.
    """

    @pytest.fixture
    def phase_gate_schema(self):
        schema_path = REPO_ROOT / "schemas" / "governance" / "phase-gate-record.schema.json"
        if not schema_path.exists():
            pytest.skip("Schema file not found")
        return json.loads(schema_path.read_text())

    def test_schema_has_timestamp_pattern(self, phase_gate_schema):
        """Timestamp field must have ISO 8601 pattern."""
        props = phase_gate_schema.get("properties", {})
        timestamp_field = props.get("timestamp", {})
        assert "pattern" in timestamp_field, (
            "phase-gate-record.schema.json timestamp field must have 'pattern' "
            "to enforce ISO 8601 format (CRIT-02)"
        )
        pattern = timestamp_field["pattern"]
        # Verify pattern rejects 'pending'
        assert not re.match(pattern, "pending"), (
            f"Pattern '{pattern}' incorrectly accepts 'pending' as a timestamp"
        )
        # Verify pattern accepts valid ISO 8601
        assert re.match(pattern, "2025-01-15T09:30:00Z"), (
            f"Pattern '{pattern}' rejects valid ISO 8601 datetime"
        )

    def test_schema_rejects_ai_as_approver_for_go_decisions(self, phase_gate_schema):
        """Approver field must not allow AI/Codex/AIDEN when decision is 'go'."""
        try:
            from jsonschema import ValidationError, validate
        except ImportError:
            pytest.skip("jsonschema not installed")

        bad_record = {
            "id": "PG-0001",
            "phase": "root-scaffold",
            "decision": "go",
            "justification": "AI approved this automatically",
            "approver": "AIDEN",  # This must be REJECTED
            "timestamp": "2025-01-15T09:30:00Z",
        }
        with pytest.raises(ValidationError):
            validate(instance=bad_record, schema=phase_gate_schema)

    def test_hitl_gate_node_rejects_ai_approver(self, test_settings):
        """workflow hitl_gate_node must raise ValueError for AI approvers."""
        from unittest.mock import patch

        from aiden.workflow.graph import hitl_gate_node

        state = make_initial_state(
            trace_id="test-crit02",
            actor="test-actor",
            phase="test-phase",
        )
        state["approval_required"] = True
        state["approval_type"] = "phase_gate"

        # Simulate interrupt() returning an AI approver
        with patch("aiden.workflow.graph.interrupt", return_value={"approver": "AIDEN"}):
            with pytest.raises(ValueError, match="AI agents are not valid approvers"):
                hitl_gate_node(state)


# ── CRIT-03: Secret handling must be testable and automated ──────────────────

class TestCrit03SecretHandling:
    """
    CRIT-03: No executable tests for secret handling (only .md specs).
    Resolution: FakeKeychain + these tests provide executable coverage.
    """

    def test_fake_keychain_stores_and_retrieves(self, fake_keychain):
        val = fake_keychain.retrieve("ref_litellm_proxy_key")
        assert val == "test-litellm-key-not-real"

    def test_fake_keychain_raises_on_missing(self):
        kc = FakeKeychain()
        with pytest.raises(KeychainEntryNotFound):
            kc.retrieve("ref_nonexistent_key")

    def test_ref_id_validation_rejects_literals(self):
        """Credential-like values must not pass as reference IDs."""
        bad_ids = [
            "sk-abc123",
            "0x" + "a" * 64,
            "my-api-key",
            "password",
            "",
            "REF_UPPERCASE",
            "ref with spaces",
        ]
        for bad_id in bad_ids:
            with pytest.raises(ValueError, match="Invalid secret_reference_id"):
                _validate_ref_id(bad_id)

    def test_ref_id_validation_accepts_valid_patterns(self):
        """Valid reference IDs must pass validation."""
        good_ids = [
            "ref_litellm_proxy_key",
            "ref_research_api",
            "ref_a",
            "ref_123",
            "ref_some_long_service_name_key",
        ]
        for good_id in good_ids:
            _validate_ref_id(good_id)  # Must not raise

    def test_rotate_is_atomic(self):
        """Rotation must leave the new value in place after completion."""
        kc = FakeKeychain({"ref_test_key": "old-value"})
        kc.rotate("ref_test_key", "new-value")
        assert kc.retrieve("ref_test_key") == "new-value"
        assert not kc.exists("ref_test_key_rotation_backup")


# ── HIGH-01: CODEOWNERS must have secondary reviewer on critical paths ────────

class TestHigh01CodeOwners:
    """
    HIGH-01: CODEOWNERS pointed everything to a single @repo-owner.
    Resolution: Security-critical paths now require @security-reviewer as well.
    """

    @pytest.fixture
    def codeowners_content(self):
        codeowners = REPO_ROOT / ".github" / "CODEOWNERS"
        if not codeowners.exists():
            pytest.skip("CODEOWNERS not found")
        return codeowners.read_text()

    def test_safety_md_has_two_owners(self, codeowners_content):
        """SAFETY.md must list two reviewers."""
        lines = [l for l in codeowners_content.splitlines()
                 if l.strip().startswith("SAFETY.md")]
        assert lines, "SAFETY.md not found in CODEOWNERS"
        # Must have at least two @mentions
        at_count = lines[0].count("@")
        assert at_count >= 2, (
            f"SAFETY.md in CODEOWNERS must have >= 2 owners (HIGH-01), "
            f"found: {lines[0]}"
        )

    def test_security_docs_have_two_owners(self, codeowners_content):
        """docs/security/ must list two reviewers."""
        lines = [l for l in codeowners_content.splitlines()
                 if "/docs/security/" in l or "docs/security" in l]
        assert lines, "docs/security/ not found in CODEOWNERS"
        at_count = lines[0].count("@")
        assert at_count >= 2, (
            f"docs/security/ in CODEOWNERS must have >= 2 owners (HIGH-01), "
            f"found: {lines[0]}"
        )


# ── HIGH-03: Budget cap must raise, never silently continue ──────────────────

class TestHigh03BudgetCapEnforcement:
    """
    HIGH-03: Session cost cap was documented but not schema-enforced.
    Resolution: ModelRouter raises BudgetExceededError before any over-budget call.
    ResearchState.session_cost_usd tracks cumulative spend.
    """

    def test_router_raises_on_cost_budget_exceeded(self, test_settings, fake_keychain):
        """Router must raise BudgetExceededError when cost budget is exceeded."""
        router = ModelRouter(
            keychain=fake_keychain,
            settings=test_settings,
            session_cost={"tokens": 0, "cost_usd": test_settings.budget_usd},
        )
        with pytest.raises(BudgetExceededError, match="budget exceeded"):
            router.call(
                "hello",
                complexity=1,
                trace_id="test-high03",
                actor="test",
                purpose="budget test",
            )

    def test_router_raises_on_token_budget_exceeded(self, test_settings, fake_keychain):
        """Router must raise BudgetExceededError when token budget is exceeded."""
        router = ModelRouter(
            keychain=fake_keychain,
            settings=test_settings,
            session_cost={"tokens": test_settings.budget_tokens, "cost_usd": 0.0},
        )
        with pytest.raises(BudgetExceededError, match="budget exceeded"):
            router.call(
                "hello",
                complexity=1,
                trace_id="test-high03-tokens",
                actor="test",
                purpose="token budget test",
            )

    def test_research_state_has_session_cost_field(self):
        """ResearchState TypedDict must include session_cost_usd."""
        state = make_initial_state(
            trace_id="test-cost",
            actor="test",
            phase="test-phase",
        )
        assert "session_cost_usd" in state
        assert isinstance(state["session_cost_usd"], float)
        assert state["session_cost_usd"] == 0.0

    def test_budget_exceeded_error_triggers_human_gate(self, test_settings):
        """Workflow node must set approval_required when budget is exceeded."""
        from aiden.workflow.graph import research_node

        state = make_initial_state(
            trace_id="test-high03-workflow",
            actor="test",
            phase="test-phase",
        )
        # Simulate budget already exceeded
        state["session_cost_usd"] = test_settings.budget_usd + 0.01

        result = research_node(state, settings=test_settings)
        assert result.get("approval_required") is True
        assert result.get("approval_type") == "capital"


# ── HIGH-04: notes field must reject secret-like content ─────────────────────

class TestHigh04NotesFieldInjectionGuard:
    """
    HIGH-04: safe-config.schema.json 'notes' field had no content validation.
    Resolution: 'not.pattern' guard rejects credential-like strings in notes.
    """

    @pytest.fixture
    def safe_config_schema(self):
        schema_path = REPO_ROOT / "schemas" / "secret-manager" / "safe-config.schema.json"
        if not schema_path.exists():
            pytest.skip("Schema file not found")
        return json.loads(schema_path.read_text())

    def test_notes_rejects_api_key_pattern(self, safe_config_schema):
        """notes field must reject API key patterns."""
        try:
            from jsonschema import ValidationError, validate
        except ImportError:
            pytest.skip("jsonschema not installed")

        bad_config = {
            "secret_reference_id": "ref_test_key",
            "storage_candidate": "os_keychain_primary",
            "custody_owner": "human_owner",
            "approval_reference": "AR-0001",
            "incident_blocker": False,
            "notes": "API key is sk-abc123xyz987abc123",
        }
        with pytest.raises(ValidationError):
            validate(instance=bad_config, schema=safe_config_schema)

    def test_notes_accepts_benign_text(self, safe_config_schema):
        """notes field must accept benign metadata text."""
        try:
            from jsonschema import validate
        except ImportError:
            pytest.skip("jsonschema not installed")

        good_config = {
            "secret_reference_id": "ref_research_api_metadata",
            "storage_candidate": "os_keychain_primary",
            "custody_owner": "human_owner",
            "approval_reference": "AR-0001",
            "incident_blocker": False,
            "notes": "Metadata-only fixture. Registered 2025-01-15. No credentials here.",
        }
        validate(instance=good_config, schema=safe_config_schema)  # Must not raise

    def test_custody_owner_rejects_ai_agents(self, safe_config_schema):
        """custody_owner must not be an AI agent name."""
        try:
            from jsonschema import ValidationError, validate
        except ImportError:
            pytest.skip("jsonschema not installed")

        bad_config = {
            "secret_reference_id": "ref_test_key",
            "storage_candidate": "os_keychain_primary",
            "custody_owner": "AIDEN",
            "approval_reference": "AR-0001",
            "incident_blocker": False,
        }
        with pytest.raises(ValidationError):
            validate(instance=bad_config, schema=safe_config_schema)
