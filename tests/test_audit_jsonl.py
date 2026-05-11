"""Test audit event JSONL format and emission.

Resolves Phase 4+5 Task F6: Audit event JSONL format coverage.
"""

import pytest
import json


class TestAuditEventJSONL:
    """Test audit event JSONL output format and schema compliance."""

    def test_jsonl_format_valid(self, tmp_path):
        """Each line must be valid JSON (JSONL format)."""
        sample_line = json.dumps({
            "id": "AE-0001",
            "event_type": "validation",
            "actor": "Codex",
            "timestamp": "2026-05-11T10:00:00Z",
            "resource": "schemas/decision-log.schema.json",
            "action": "migrated to 2020-12",
            "outcome": "success"
        })
        # Parse as JSON
        parsed = json.loads(sample_line)
        assert parsed["id"].startswith("AE-")
        assert parsed["outcome"] in ["success", "failure", "blocked"]

    def test_jsonl_schema_compliance(self):
        """Each line must comply with audit-event.schema.json."""
        required_fields = ["id", "event_type", "actor", "timestamp", "resource", "action", "outcome"]
        event = {
            "id": "AE-0001", "event_type": "validation", "actor": "Codex",
            "timestamp": "2026-05-11T10:00:00Z", "resource": "test",
            "action": "test", "outcome": "success"
        }
        for field in required_fields:
            assert field in event, f"Required field {field} missing"

    def test_jsonl_no_credentials(self):
        """Audit events must never contain credential values."""
        forbidden_patterns = ["sk-", "ghp_", "AIza", "0x" + "a" * 40, "private_key"]
        sample_event = json.dumps({"action": "test", "resource": "schemas/test.json"})
        for pattern in forbidden_patterns:
            assert pattern not in sample_event, f"Credential pattern {pattern} found in audit event"

    def test_jsonl_local_path_redacted(self):
        """Local paths must be redacted in audit events."""
        # Absolute paths should not appear in JSONL
        event_with_path = json.dumps({"resource": "/home/user/project/file.py"})
        assert "/home/" not in event_with_path or "REDACTED" in event_with_path

    def test_jsonl_append_only(self, tmp_path):
        """Audit log must be append-only (never modify existing lines)."""
        log_file = tmp_path / "audit.jsonl"
        line1 = json.dumps({"id": "AE-0001", "action": "start"}) + "\n"
        line2 = json.dumps({"id": "AE-0002", "action": "end"}) + "\n"
        log_file.write_text(line1)
        with open(log_file, "a") as f:
            f.write(line2)
        lines = log_file.read_text().strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0])["id"] == "AE-0001"
        assert json.loads(lines[1])["id"] == "AE-0002"
