"""
aiden.observability.tracer
~~~~~~~~~~~~~~~~~~~~~~~~~~
Audit event emission with Langfuse + local JSONL fallback.

Rules:
  - Conforms to schemas/research-lab/audit-event.schema.json
  - JSONL file stays local-only (gitignored). Never promoted to GitHub.
  - Raw reasoning_trace is NEVER written to the JSONL when observability is disabled.
  - No-op when AIDEN_OBSERVABILITY_ENABLED=false (for test isolation).
"""

from __future__ import annotations

import json
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import structlog

log = structlog.get_logger(__name__)

# Matches schemas/research-lab/audit-event.schema.json
_REQUIRED_FIELDS = {"trace_id", "actor", "event", "governance_policy", "result"}


@dataclass
class AuditEvent:
    """
    Structured audit event.
    reasoning_trace is local-only and never promoted to GitHub artifacts.
    """

    trace_id: str
    actor: str
    event: str
    governance_policy: str
    result: str
    approval_reference: str = ""
    reasoning_trace: str = ""   # LOCAL ONLY — never included in GitHub summaries
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_jsonl_dict(self) -> dict[str, Any]:
        """Serialise for local JSONL log. Includes reasoning_trace."""
        d = asdict(self)
        d["timestamp"] = datetime.now(timezone.utc).isoformat()
        return {k: v for k, v in d.items() if v or k in _REQUIRED_FIELDS}

    def to_github_summary_dict(self) -> dict[str, Any]:
        """
        Serialise for GitHub-promotable summaries.
        reasoning_trace is STRIPPED per LOCAL_STORAGE_SOP.md.
        """
        d = self.to_jsonl_dict()
        d.pop("reasoning_trace", None)
        d.pop("metadata", None)
        return d


class _NullTracer:
    """No-op tracer used when AIDEN_OBSERVABILITY_ENABLED=false."""

    def emit(self, event: AuditEvent) -> None:
        pass

    def flush(self) -> None:
        pass


class JsonlTracer:
    """
    Writes audit events to a local JSONL file.
    Thread-safe. File path must be outside tracked repository directories.
    """

    def __init__(self, audit_path: Path) -> None:
        self._path = audit_path
        self._lock = threading.Lock()
        audit_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: AuditEvent) -> None:
        line = json.dumps(event.to_jsonl_dict(), ensure_ascii=False)
        with self._lock:
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")

    def flush(self) -> None:
        pass  # File writes are synchronous


class LangfuseTracer:
    """
    Langfuse-backed tracer with JSONL fallback on connection failure.
    Lazy-imports langfuse so the package is optional at import time.
    """

    def __init__(self, jsonl_fallback: JsonlTracer) -> None:
        self._fallback = jsonl_fallback
        self._client: Any = None
        self._init_attempted = False

    def _get_client(self) -> Any | None:
        if self._init_attempted:
            return self._client
        self._init_attempted = True
        try:
            from langfuse import Langfuse  # noqa: PLC0415
            self._client = Langfuse()
            log.info("langfuse.connected")
        except Exception as exc:
            log.warning("langfuse.unavailable", error=str(exc))
            self._client = None
        return self._client

    def emit(self, event: AuditEvent) -> None:
        client = self._get_client()
        try:
            if client is not None:
                client.trace(
                    name=event.event,
                    user_id=event.actor,
                    session_id=event.trace_id,
                    metadata=event.to_github_summary_dict(),
                )
        except Exception as exc:
            log.warning("langfuse.emit_failed", error=str(exc))
        # Always write to JSONL as well (belt-and-suspenders)
        self._fallback.emit(event)

    def flush(self) -> None:
        try:
            if self._client is not None:
                self._client.flush()
        except Exception:
            pass
        self._fallback.flush()


# ── Module-level tracer (lazy initialisation) ────────────────────────────────
_tracer: _NullTracer | JsonlTracer | LangfuseTracer | None = None
_tracer_lock = threading.Lock()


def _build_tracer() -> _NullTracer | JsonlTracer | LangfuseTracer:
    from aiden.config.settings import get_settings  # noqa: PLC0415 — avoid circular import at module level
    cfg = get_settings()

    if not cfg.observability_enabled:
        return _NullTracer()

    jsonl = JsonlTracer(cfg.jsonl_audit_path)
    return LangfuseTracer(jsonl_fallback=jsonl)


def _get_tracer() -> _NullTracer | JsonlTracer | LangfuseTracer:
    global _tracer
    if _tracer is None:
        with _tracer_lock:
            if _tracer is None:
                _tracer = _build_tracer()
    return _tracer


def emit_audit_event(event: AuditEvent) -> None:
    """Emit a single audit event through the active tracer."""
    _get_tracer().emit(event)


def flush_tracer() -> None:
    """Flush buffered events. Call at application shutdown."""
    _get_tracer().flush()


def reset_tracer() -> None:
    """Reset tracer singleton. Use in tests after overriding settings."""
    global _tracer
    with _tracer_lock:
        _tracer = None
