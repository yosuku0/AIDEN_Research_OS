"""
aiden.secrets.keychain
~~~~~~~~~~~~~~~~~~~~~~
OS Keychain adapter (ADR-0016, ADR-0017).

Design rules:
  1. The adapter stores and retrieves values using OPAQUE reference IDs only.
     It NEVER logs the resolved credential value.
  2. reference_id must match ^ref_[a-z0-9_]+$ — enforced at runtime.
  3. The SERVICE_NAME namespace isolates AIDEN keys from other system keys.
  4. Tests use FakeKeychain (in-memory dict) to avoid touching the real OS keychain.
  5. Rotation is atomic: store new → verify retrieve → delete old backup.
"""

from __future__ import annotations

import re
import threading
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

import structlog

log = structlog.get_logger(__name__)

# Namespace in the OS keychain — all AIDEN secrets are stored under this service
SERVICE_NAME = "aiden-research-os"

# Reference ID validation pattern (mirrors schemas/secret-manager/safe-config.schema.json)
_REF_ID_PATTERN = re.compile(r"^ref_[a-z0-9_]+$")


def _validate_ref_id(ref_id: str) -> None:
    """Raise ValueError if ref_id does not meet the naming convention."""
    if not _REF_ID_PATTERN.match(ref_id):
        raise ValueError(
            f"Invalid secret_reference_id: '{ref_id}'. "
            f"Must match ^ref_[a-z0-9_]+$  (e.g. 'ref_litellm_proxy_key'). "
            f"This field must be an opaque reference, never the credential value itself."
        )


@runtime_checkable
class KeychainAdapter(Protocol):
    """Interface contract for all keychain backends."""

    def store(self, ref_id: str, value: str, *, trace_id: str = "") -> None:
        """Store a credential value under ref_id."""
        ...

    def retrieve(self, ref_id: str, *, trace_id: str = "") -> str:
        """Retrieve a credential value by ref_id. Raises KeychainEntryNotFound if absent."""
        ...

    def delete(self, ref_id: str, *, trace_id: str = "") -> None:
        """Delete a credential value by ref_id."""
        ...

    def rotate(self, ref_id: str, new_value: str, *, trace_id: str = "") -> None:
        """Atomically replace a credential. store new → verify → delete old backup."""
        ...

    def exists(self, ref_id: str) -> bool:
        """Return True if a credential exists for ref_id."""
        ...


class KeychainEntryNotFound(Exception):
    """Raised when a ref_id has no associated entry in the keychain."""

    def __init__(self, ref_id: str) -> None:
        super().__init__(f"No keychain entry found for reference: '{ref_id}'")
        self.ref_id = ref_id


class OsKeychainAdapter:
    """
    Production adapter backed by the OS keychain via the `keyring` library.

    Supported backends (selected automatically by keyring):
      - macOS   : Keychain
      - Windows : Windows Credential Manager
      - Linux   : SecretService (e.g. GNOME Keyring, KWallet)

    NEVER store the returned value in a variable that gets logged or serialised.
    """

    def __init__(self, service_name: str = SERVICE_NAME) -> None:
        self._service = service_name
        try:
            import keyring  # noqa: PLC0415
            self._keyring = keyring
        except ImportError as exc:
            raise ImportError(
                "The 'keyring' package is required for OsKeychainAdapter. "
                "Install it with: pip install keyring"
            ) from exc

    def store(self, ref_id: str, value: str, *, trace_id: str = "") -> None:
        _validate_ref_id(ref_id)
        self._keyring.set_password(self._service, ref_id, value)
        # Log ref_id only — NEVER log value
        log.info("keychain.store", ref_id=ref_id, trace_id=trace_id or "—")

    def retrieve(self, ref_id: str, *, trace_id: str = "") -> str:
        _validate_ref_id(ref_id)
        result = self._keyring.get_password(self._service, ref_id)
        if result is None:
            log.warning("keychain.miss", ref_id=ref_id, trace_id=trace_id or "—")
            raise KeychainEntryNotFound(ref_id)
        # Log only that retrieval succeeded — not the value
        log.info("keychain.retrieve.ok", ref_id=ref_id, trace_id=trace_id or "—")
        return result

    def delete(self, ref_id: str, *, trace_id: str = "") -> None:
        _validate_ref_id(ref_id)
        try:
            self._keyring.delete_password(self._service, ref_id)
        except Exception:
            pass  # Already absent is fine
        log.info("keychain.delete", ref_id=ref_id, trace_id=trace_id or "—")

    def rotate(self, ref_id: str, new_value: str, *, trace_id: str = "") -> None:
        """Atomic rotation: store under backup key → overwrite primary → delete backup."""
        _validate_ref_id(ref_id)
        backup_ref = f"{ref_id}_rotation_backup"
        _validate_ref_id(backup_ref)

        # 1. Backup current value
        try:
            current = self.retrieve(ref_id, trace_id=trace_id)
            self.store(backup_ref, current, trace_id=trace_id)
        except KeychainEntryNotFound:
            pass  # No existing value — rotation is a first-time store

        # 2. Store new value
        self.store(ref_id, new_value, trace_id=trace_id)

        # 3. Verify new value is retrievable
        check = self.retrieve(ref_id, trace_id=trace_id)
        if check != new_value:  # noqa: S105 — constant time compare not needed; value not logged
            raise RuntimeError(
                f"Keychain rotation verify failed for '{ref_id}'. "
                f"Backup key '{backup_ref}' still holds previous value."
            )

        # 4. Delete backup
        self.delete(backup_ref, trace_id=trace_id)
        log.info("keychain.rotate.complete", ref_id=ref_id, trace_id=trace_id or "—")

    def exists(self, ref_id: str) -> bool:
        _validate_ref_id(ref_id)
        try:
            return self._keyring.get_password(self._service, ref_id) is not None
        except Exception:
            return False


class FakeKeychain:
    """
    In-memory keychain backend for unit tests.

    Usage:
        from aiden.secrets.keychain import FakeKeychain
        adapter = FakeKeychain({"ref_litellm_proxy_key": "test-value"})
        adapter.retrieve("ref_litellm_proxy_key")  # → "test-value"

    NEVER use in production. The _store dict is not encrypted.
    """

    def __init__(self, initial: dict[str, str] | None = None) -> None:
        self._lock = threading.Lock()
        self._store: dict[str, str] = dict(initial or {})

    def store(self, ref_id: str, value: str, *, trace_id: str = "") -> None:
        _validate_ref_id(ref_id)
        with self._lock:
            self._store[ref_id] = value

    def retrieve(self, ref_id: str, *, trace_id: str = "") -> str:
        _validate_ref_id(ref_id)
        with self._lock:
            if ref_id not in self._store:
                raise KeychainEntryNotFound(ref_id)
            return self._store[ref_id]

    def delete(self, ref_id: str, *, trace_id: str = "") -> None:
        _validate_ref_id(ref_id)
        with self._lock:
            self._store.pop(ref_id, None)

    def rotate(self, ref_id: str, new_value: str, *, trace_id: str = "") -> None:
        _validate_ref_id(ref_id)
        with self._lock:
            self._store[ref_id] = new_value

    def exists(self, ref_id: str) -> bool:
        _validate_ref_id(ref_id)
        with self._lock:
            return ref_id in self._store

    def snapshot(self) -> dict[str, str]:
        """Return a copy of the current store. For test assertions ONLY."""
        with self._lock:
            return dict(self._store)
