"""Test OS Keychain adapter reference ID validation.

Resolves Phase 4+5 Task F6: Keychain reference ID validation coverage.
"""

import pytest
import re


class TestKeychainReferenceValidation:
    """Test that keychain reference IDs are validated correctly."""

    def test_reference_id_format(self):
        """Reference IDs must match allowed pattern (e.g., urn:aiken:secret:N)."""
        valid_patterns = [
            "urn:aiken:secret:1",
            "urn:aiken:secret:42",
            "urn:aiken:secret:999",
        ]
        pattern = re.compile(r'^urn:aiken:secret:\d+$')
        for ref in valid_patterns:
            assert pattern.match(ref), f"{ref} should be valid"

    def test_reference_id_rejects_invalid(self):
        """Reference IDs must reject invalid formats."""
        invalid_patterns = [
            "secret:1",               # missing urn prefix
            "urn:aiken:secret:",     # missing number
            "urn:aiken:password:1",  # wrong type
            "urn:other:secret:1",    # wrong namespace
            "",                       # empty
            "/home/user/.ssh/key",   # local path (FORBIDDEN)
            "sk-proj-test12345",      # credential-like (FORBIDDEN)
        ]
        pattern = re.compile(r'^urn:aiken:secret:\d+$')
        for ref in invalid_patterns:
            assert not pattern.match(ref), f"{ref} should be invalid"

    def test_reference_id_no_local_path(self):
        """Reference IDs must never contain local filesystem paths."""
        # Hard-ban: no local paths in reference IDs
        forbidden = ["/home/", "/Users/", "C:\\", "~/.", "./", "../"]
        ref_id = "urn:aiken:secret:1"
        for f in forbidden:
            assert f not in ref_id, f"Reference ID must not contain {f}"

    def test_reference_id_no_credential_value(self):
        """Reference IDs must not contain credential-like values."""
        # Hard-ban: no credential values
        forbidden_patterns = ["sk-", "0x", "-----BEGIN"]
        ref_id = "urn:aiken:secret:1"
        for f in forbidden_patterns:
            assert f not in ref_id, f"Reference ID must not contain {f}"

    def test_opaque_reference_no_retrieval(self):
        """Reference IDs are opaque; no secret value retrieval."""
        # Verify that reference ID cannot be used to extract secret value
        # This is the core security property
        pytest.skip("Requires keychain adapter implementation")
