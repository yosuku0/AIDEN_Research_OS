"""
tests/conftest.py
~~~~~~~~~~~~~~~~~
Shared pytest fixtures for the aiden-core test suite.

All fixtures use:
  - FakeKeychain (in-memory, never touches real OS keychain)
  - AIDEN_OBSERVABILITY_ENABLED=false (prevents JSONL writes during tests)
  - AidenSettings overrides for deterministic budget values
"""

from __future__ import annotations

import os
import uuid
from typing import Generator

import pytest

# ── Force test environment BEFORE any aiden imports ─────────────────────────
os.environ.setdefault("AIDEN_OBSERVABILITY_ENABLED", "false")
os.environ.setdefault("AIDEN_ENV", "test")
os.environ.setdefault("AIDEN_LOG_LEVEL", "WARNING")


from aiden.config.settings import AidenSettings, override_settings, reset_settings
from aiden.observability.tracer import reset_tracer
from aiden.secrets.keychain import FakeKeychain


# ── Settings fixtures ─────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def _reset_singletons() -> Generator[None, None, None]:
    """
    Auto-use fixture that resets all module singletons between tests.
    Prevents settings / tracer state leaking between test cases.
    """
    yield
    reset_settings()
    reset_tracer()


@pytest.fixture
def test_settings() -> AidenSettings:
    """
    AidenSettings with safe, deterministic values for testing.
    Budget is set low to make budget-cap tests fast.
    """
    cfg = AidenSettings(
        env="test",
        observability_enabled=False,
        jsonl_audit_path="local/test-audit.jsonl",  # Written only if enabled
        local_model_url="http://localhost:11434",
        litellm_proxy_url="http://localhost:4000",
        budget_usd=0.10,      # Low budget for budget-cap tests
        budget_tokens=1_000,
        max_steps=5,          # Short for fast workflow tests
        circuit_breaker_turns=3,
        log_level="WARNING",
    )
    override_settings(cfg)
    return cfg


# ── Secret fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def fake_keychain() -> FakeKeychain:
    """
    In-memory FakeKeychain pre-populated with test reference IDs.
    Keys follow the ^ref_[a-z0-9_]+$ convention.
    Values are synthetic and non-functional.
    """
    return FakeKeychain({
        "ref_litellm_proxy_key": "test-litellm-key-not-real",
        "ref_research_api_metadata": "test-metadata-ref",
    })


# ── Trace ID fixture ──────────────────────────────────────────────────────────

@pytest.fixture
def trace_id() -> str:
    """Unique trace ID for each test case."""
    return f"test-{uuid.uuid4().hex[:8]}"


# ── Audit event collector ─────────────────────────────────────────────────────

class AuditEventCollector:
    """Collects AuditEvents emitted during a test for assertion."""

    def __init__(self) -> None:
        self.events: list[dict] = []

    def record(self, event: object) -> None:
        if hasattr(event, "to_jsonl_dict"):
            self.events.append(event.to_jsonl_dict())

    def find(self, event_name: str) -> list[dict]:
        return [e for e in self.events if e.get("event") == event_name]

    def assert_has_event(self, event_name: str) -> None:
        matches = self.find(event_name)
        assert matches, (
            f"Expected audit event '{event_name}' but not found. "
            f"Recorded events: {[e.get('event') for e in self.events]}"
        )

    def assert_no_secrets(self) -> None:
        """Assert that no audit event contains secret-like patterns."""
        import re
        secret_re = re.compile(
            r"(sk-[a-zA-Z0-9]{10,}|0x[0-9a-fA-F]{40,}|-----BEGIN|password=\S+)"
        )
        for event in self.events:
            serialised = str(event)
            match = secret_re.search(serialised)
            assert match is None, (
                f"Secret-like pattern detected in audit event: {match.group()!r}\n"
                f"Event: {event}"
            )
