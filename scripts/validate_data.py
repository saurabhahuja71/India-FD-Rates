#!/usr/bin/env python3
"""Fail closed if the published FD snapshot is malformed."""
import json, sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data/fd-rates.json"
ALLOWED = {"private_sector", "public_sector", "small_finance"}
try:
    data = json.loads(DATA.read_text())
    assert isinstance(data["generated_at"], str) and data["rows"]
    assert len(data["rows"]) >= 15
    statuses = {"VERIFIED", "STALE", "FAILED", "SAMPLE"}
    for row in data["rows"]:
        assert row["category"] in ALLOWED and row["bank_name"] and row["source_url"].startswith("https://")
        assert row["deposit_category"] and row["deposit_limit"]
        assert row["status"] in statuses and row["source_type"] and isinstance(row["evidence"], dict)
        assert {"matched_tenure", "matched_regular_rate", "matched_senior_rate"} <= set(row["evidence"])
        if row["status"] == "VERIFIED":
            assert 0 < float(row["regular_rate"]) <= 15 and 0 < float(row["senior_rate"]) <= 15
            assert row["regular_tenure"] and row["senior_tenure"] and row["verified_at"]
            assert row["evidence"]["matched_regular_rate"] and row["evidence"]["matched_senior_rate"]
except (AssertionError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
    print(f"Invalid FD data: {exc}", file=sys.stderr); sys.exit(1)
print(f"Validated {len(data['rows'])} FD rate rows")
