"""
aiden.models.router
~~~~~~~~~~~~~~~~~~~
Local-first LiteLLM model router with cost circuit breaker.

Implements CLOUD_LOCAL_SPLIT.md, MODEL_ROUTING_COST_LIMITS.md, TECH_STACK_MATRIX.md:
  - Complexity 0-2 → Ollama local (no API cost)
  - Complexity 3-4 → LiteLLM Proxy (cloud escalation)
  - Budget exceeded → BudgetExceededError (never silently continues)
  - API keys retrieved via KeychainAdapter (never literals)
  - Every call emits an AuditEvent
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import structlog

from aiden.config.settings import AidenSettings, get_settings
from aiden.observability.tracer import AuditEvent, emit_audit_event
from aiden.secrets.keychain import FakeKeychain, KeychainAdapter

log = structlog.get_logger(__name__)


class BudgetExceededError(Exception):
    """Raised when a model call would exceed the per-session cost or token budget."""

    def __init__(
        self,
        *,
        current_cost: float,
        budget_usd: float,
        current_tokens: int,
        budget_tokens: int,
        trace_id: str = "",
    ) -> None:
        super().__init__(
            f"Session budget exceeded: ${current_cost:.4f} / ${budget_usd:.2f} USD, "
            f"{current_tokens} / {budget_tokens} tokens. "
            f"[HUMAN GATE] Capital approval required. trace_id={trace_id}"
        )
        self.current_cost = current_cost
        self.budget_usd = budget_usd
        self.current_tokens = current_tokens
        self.budget_tokens = budget_tokens
        self.trace_id = trace_id


@dataclass
class ModelCallResult:
    """Result of a single model invocation."""

    content: str
    model_used: str
    tokens_used: int
    cost_usd: float
    is_local: bool


def _estimate_cost(model: str, tokens: int) -> float:
    """
    Rough cost estimate for budget tracking.
    Override with actual LiteLLM cost data in production.
    """
    # Local models are free
    if model.startswith("ollama/") or model.startswith("ollama_chat/"):
        return 0.0
    # Rough cloud estimates (update when LiteLLM provides real costs)
    cost_per_1k = {
        "claude-sonnet": 0.003,
        "gpt-4": 0.010,
        "gemini-2.5-pro": 0.002,
    }
    for key, rate in cost_per_1k.items():
        if key in model:
            return (tokens / 1000) * rate
    return (tokens / 1000) * 0.002  # Conservative default


class ModelRouter:
    """
    Routes model calls based on complexity score with cost circuit breaker.

    Args:
        keychain:       KeychainAdapter for retrieving LiteLLM proxy API key.
        settings:       AidenSettings instance.
        session_cost:   Mutable dict tracking {"tokens": int, "cost_usd": float}.
                        Pass the same dict across calls within one workflow session.
    """

    # Complexity thresholds (from TECH_STACK_MATRIX.md / CLOUD_LOCAL_SPLIT.md)
    LOCAL_MAX_COMPLEXITY = 2
    CLOUD_MIN_COMPLEXITY = 3

    def __init__(
        self,
        *,
        keychain: KeychainAdapter | None = None,
        settings: AidenSettings | None = None,
        session_cost: dict[str, Any] | None = None,
    ) -> None:
        self._cfg = settings or get_settings()
        self._keychain = keychain or FakeKeychain()
        self._session: dict[str, Any] = session_cost or {"tokens": 0, "cost_usd": 0.0}

    # ── Public API ───────────────────────────────────────────────────────────

    def call(
        self,
        prompt: str,
        *,
        complexity: int,
        trace_id: str,
        actor: str,
        purpose: str,
        system: str | None = None,
    ) -> ModelCallResult:
        """
        Route and execute a model call.

        Args:
            prompt:     User message content.
            complexity: 0-4 score. 0-2 = local, 3-4 = cloud.
            trace_id:   Audit trace identifier.
            actor:      Human or agent identity making the call.
            purpose:    Human-readable purpose (logged, not sent to model).
            system:     Optional system message.

        Raises:
            BudgetExceededError: If session budget would be exceeded.
        """
        self._check_budget(trace_id=trace_id)

        is_local = complexity <= self.LOCAL_MAX_COMPLEXITY
        model = self._select_model(complexity)

        emit_audit_event(AuditEvent(
            trace_id=trace_id,
            actor=actor,
            event="model_router.call.start",
            governance_policy="CLOUD_LOCAL_SPLIT",
            result=f"routing_to:{model}",
            metadata={
                "complexity": complexity,
                "is_local": is_local,
                "purpose": purpose,
                "model": model,
            },
        ))

        try:
            result = self._invoke(
                model=model,
                prompt=prompt,
                system=system,
                is_local=is_local,
                trace_id=trace_id,
            )
        except Exception as exc:
            emit_audit_event(AuditEvent(
                trace_id=trace_id,
                actor=actor,
                event="model_router.call.error",
                governance_policy="CLOUD_LOCAL_SPLIT",
                result=f"error:{type(exc).__name__}",
            ))
            raise

        # Update session accounting
        self._session["tokens"] += result.tokens_used
        self._session["cost_usd"] += result.cost_usd

        emit_audit_event(AuditEvent(
            trace_id=trace_id,
            actor=actor,
            event="model_router.call.complete",
            governance_policy="MODEL_ROUTING_COST_LIMITS",
            result="ok",
            metadata={
                "tokens_used": result.tokens_used,
                "cost_usd": result.cost_usd,
                "cumulative_tokens": self._session["tokens"],
                "cumulative_cost_usd": self._session["cost_usd"],
            },
        ))

        return result

    @property
    def session_tokens(self) -> int:
        return self._session["tokens"]

    @property
    def session_cost_usd(self) -> float:
        return self._session["cost_usd"]

    # ── Private helpers ──────────────────────────────────────────────────────

    def _check_budget(self, *, trace_id: str) -> None:
        """Raise BudgetExceededError before making a call that would exceed budget."""
        if self._session["cost_usd"] >= self._cfg.budget_usd:
            emit_audit_event(AuditEvent(
                trace_id=trace_id,
                actor="model_router",
                event="model_router.budget.exceeded",
                governance_policy="MODEL_ROUTING_COST_LIMITS",
                result="rejected",
            ))
            raise BudgetExceededError(
                current_cost=self._session["cost_usd"],
                budget_usd=self._cfg.budget_usd,
                current_tokens=self._session["tokens"],
                budget_tokens=self._cfg.budget_tokens,
                trace_id=trace_id,
            )
        if self._session["tokens"] >= self._cfg.budget_tokens:
            emit_audit_event(AuditEvent(
                trace_id=trace_id,
                actor="model_router",
                event="model_router.token_budget.exceeded",
                governance_policy="MODEL_ROUTING_COST_LIMITS",
                result="rejected",
            ))
            raise BudgetExceededError(
                current_cost=self._session["cost_usd"],
                budget_usd=self._cfg.budget_usd,
                current_tokens=self._session["tokens"],
                budget_tokens=self._cfg.budget_tokens,
                trace_id=trace_id,
            )

    def _select_model(self, complexity: int) -> str:
        """Select model identifier based on complexity score."""
        if complexity <= self.LOCAL_MAX_COMPLEXITY:
            return f"ollama_chat/{self._cfg.local_model_default}"
        # Cloud: retrieve routing via LiteLLM proxy
        # The proxy itself handles model selection; we just route to the proxy
        return "litellm_proxy/claude-sonnet"

    def _invoke(
        self,
        *,
        model: str,
        prompt: str,
        system: str | None,
        is_local: bool,
        trace_id: str,
    ) -> ModelCallResult:
        """
        Execute the actual model call via litellm.
        For local models, no API key is needed.
        For cloud models, API key is retrieved from the keychain.
        """
        try:
            import litellm  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(
                "litellm is required for ModelRouter. "
                "Install with: pip install litellm"
            ) from exc

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        call_kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
        }

        if not is_local:
            # Retrieve API key from keychain — never from env vars or literals
            try:
                api_key = self._keychain.retrieve(
                    self._cfg.litellm_api_key_ref,
                    trace_id=trace_id,
                )
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to retrieve LiteLLM API key from keychain "
                    f"(ref: {self._cfg.litellm_api_key_ref}). "
                    f"Register the key with: aiden secrets store {self._cfg.litellm_api_key_ref}"
                ) from exc

            call_kwargs["api_key"] = api_key
            call_kwargs["api_base"] = self._cfg.litellm_proxy_url

        response = litellm.completion(**call_kwargs)

        content = response.choices[0].message.content or ""
        tokens = response.usage.total_tokens if response.usage else len(prompt.split()) * 2
        cost = _estimate_cost(model, tokens)

        return ModelCallResult(
            content=content,
            model_used=model,
            tokens_used=tokens,
            cost_usd=cost,
            is_local=is_local,
        )
