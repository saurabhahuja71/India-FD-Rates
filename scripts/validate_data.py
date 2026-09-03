#!/usr/bin/env python3
"""Fail closed if the published FD snapshot is malformed."""
import json, sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data/fd-rates.json"
ALLOWED = {"private", "public", "small-finance"}
try:
    data = json.loads(DATA.read_text())
    assert isinstance(data["generated_at"], str) and data["rows"]
    assert len(data["rows"]) >= 15
    for row in data["rows"]:
        assert row["category"] in ALLOWED and row["bank"] and row["source"].startswith("https://")
        assert 0 < float(row["regular"]["rate"]) <= 15
        assert 0 < float(row["senior"]["rate"]) <= 15
        assert row["regular"]["tenure"] and row["senior"]["tenure"] and row["last_updated"]
except (AssertionError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
    print(f"Invalid FD data: {exc}", file=sys.stderr); sys.exit(1)
print(f"Validated {len(data['rows'])} FD rate rows")
