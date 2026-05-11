"""
aiden.config.settings
~~~~~~~~~~~~~~~~~~~~~
Application configuration using Pydantic BaseSettings.

SECURITY RULE: This module MUST NOT contain literal API keys, passwords,
seed phrases, or private keys. All credential access goes through
aiden.secrets.keychain.KeychainAdapter.

Environment variables accepted (all optional with safe defaults):
    AIDEN_OBSERVABILITY_ENABLED   true/false (default: true)
    AIDEN_LOCAL_MODEL_URL         Ollama base URL (default: http://localhost:11434)
    AIDEN_LITELLM_PROXY_URL       LiteLLM proxy base URL (default: http://localhost:4000)
    AIDEN_MAX_STEPS               Max workflow steps (default: 15, hard cap: 15)
    AIDEN_BUDGET_USD              Per-session cost cap (default: 1.00)
    AIDEN_BUDGET_TOKENS           Per-session token cap (default: 50000)
    AIDEN_LOG_LEVEL               Log level (default: INFO)
    AIDEN_JSONL_AUDIT_PATH        Local JSONL audit log path (default: local/audit.jsonl)
    AIDEN_ENV                     Environment: dev/test/prod (default: dev)
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AidenSettings(BaseSettings):
    """
    AIDEN Research OS runtime configuration.
    All credential material is accessed via KeychainAdapter, never stored here.
    """

    model_config = SettingsConfigDict(
        env_prefix="AIDEN_",
        env_file=".env",           # .env is gitignored; safe for local dev only
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Environment ─────────────────────────────────────────────────────────
    env: Literal["dev", "test", "prod"] = Field(
        default="dev",
        description="Deployment environment. 'prod' enables stricter enforcement.",
    )

    # ── Observability ────────────────────────────────────────────────────────
    observability_enabled: bool = Field(
        default=True,
        description="Enable Langfuse + JSONL audit tracing. Set false in tests.",
    )
    jsonl_audit_path: Path = Field(
        default=Path("local/audit.jsonl"),
        description="Local-only JSONL audit log. Never promoted to GitHub.",
    )

    # ── Local inference ──────────────────────────────────────────────────────
    local_model_url: str = Field(
        default="http://localhost:11434",
        description="Ollama base URL. No credentials required for local endpoint.",
    )
    local_model_default: str = Field(
        default="llama3.1:8b",
        description="Default local model identifier for low-complexity tasks.",
    )

    # ── Cloud routing ────────────────────────────────────────────────────────
    litellm_proxy_url: str = Field(
        default="http://localhost:4000",
        description="LiteLLM proxy base URL. API key retrieved via KeychainAdapter.",
    )
    # Keychain reference IDs — these are opaque refs, not the actual keys
    litellm_api_key_ref: str = Field(
        default="ref_litellm_proxy_key",
        pattern=r"^ref_[a-z0-9_]+$",
        description="Keychain reference for LiteLLM proxy API key.",
    )

    # ── Budget enforcement (ADR-0011, TECH_STACK_MATRIX) ────────────────────
    budget_usd: float = Field(
        default=1.00,
        ge=0.01,
        le=100.00,
        description="Per-session cost cap in USD. Router raises BudgetExceededError if exceeded.",
    )
    budget_tokens: int = Field(
        default=50_000,
        ge=1_000,
        le=1_000_000,
        description="Per-session token cap. Enforced before every model call.",
    )

    # ── Workflow limits ──────────────────────────────────────────────────────
    max_steps: int = Field(
        default=15,
        ge=1,
        le=15,
        description="Max LangGraph steps per workflow. Hard cap is 15 per TECH_STACK_MATRIX.",
    )
    circuit_breaker_turns: int = Field(
        default=3,
        ge=2,
        le=10,
        description="Number of turns for hash-based circuit breaker comparison.",
    )

    # ── Logging ──────────────────────────────────────────────────────────────
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Application log level.",
    )

    # ── Validators ───────────────────────────────────────────────────────────

    @field_validator("jsonl_audit_path", mode="before")
    @classmethod
    def validate_audit_path_not_in_repo(cls, v: object) -> object:
        """Prevent audit logs from being written into tracked repo directories."""
        path = Path(str(v))
        forbidden_prefixes = ("docs/", "research/", "schemas/", "packages/", ".github/")
        for prefix in forbidden_prefixes:
            if str(path).startswith(prefix):
                raise ValueError(
                    f"JSONL audit path '{path}' must not be inside a tracked directory. "
                    f"Use 'local/' or an absolute path outside the repository."
                )
        return v

    @field_validator("env", mode="after")
    @classmethod
    def warn_if_prod(cls, v: str) -> str:
        if v == "prod":
            import warnings
            warnings.warn(
                "AIDEN_ENV=prod is set. Ensure all Human gates are closed before "
                "production operations.",
                stacklevel=2,
            )
        return v


# Module-level singleton (lazy to allow test override)
_settings: AidenSettings | None = None


def get_settings() -> AidenSettings:
    """Return the module-level settings singleton."""
    global _settings
    if _settings is None:
        _settings = AidenSettings()
    return _settings


def override_settings(new_settings: AidenSettings) -> None:
    """Replace the settings singleton. Use only in tests."""
    global _settings
    _settings = new_settings


def reset_settings() -> None:
    """Reset settings singleton to force re-read from environment. Use in tests."""
    global _settings
    _settings = None
