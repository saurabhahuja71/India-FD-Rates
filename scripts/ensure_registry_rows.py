#!/usr/bin/env python3
"""Create non-current registry rows for newly added adapters without inventing rates."""
import json
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
data_path = root / "data/fd-rates.json"
data = json.loads(data_path.read_text())
for row in data["rows"]:
    if row["bank_name"] == "YES BANK": row["bank_name"] = "Yes Bank"
deduped = {}
for row in data["rows"]: deduped[row["bank_name"]] = row
data["rows"] = list(deduped.values())
existing = {r["bank_name"] for r in data["rows"]}
for cfg in yaml.safe_load((root / "config/banks.yaml").read_text())["banks"]:
    if cfg["name"] in existing:
        continue
    data["rows"].append({"bank_name":cfg["name"],"category":cfg["category"],"status":"SAMPLE","regular_rate":None,"regular_tenure":None,"senior_rate":None,"senior_tenure":None,"effective_date":None,"verified_at":None,"source_url":cfg["official_sources"][0]["url"],"source_type":"official_bank_website","evidence":{"matched_tenure":None,"matched_regular_rate":None,"matched_senior_rate":None},"deposit_category":cfg["deposit_category"],"deposit_limit":cfg["retail_threshold"],"notes":"Awaiting exact extraction by the configured official-source adapter."})
data_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
