#!/usr/bin/env python3
"""Generate auditable rankings and an all-bank inventory from the snapshot."""
import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/fd-rates.json"
AUDIT = ROOT / "data/ranking_audit.json"
INVENTORY = ROOT / "all-banks.html"

def main():
    snapshot = json.loads(DATA.read_text())
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    audits = []
    for category in ("private_sector", "public_sector", "small_finance"):
        candidates = [r for r in snapshot["rows"] if r["category"] == category]
        verified = sorted((r for r in candidates if r["status"] == "VERIFIED" and r.get("product_type", "STANDARD_FD") == "STANDARD_FD"), key=lambda r: (-r["regular_rate"], r["bank_name"]))
        audits.append({"category": category, "ranking_type": "standard_retail_fd", "generated_at": now, "banks": [{"rank": i, "bank": r["bank_name"], "rate": r["regular_rate"], "status": r["status"]} for i, r in enumerate(verified, 1)], "excluded": [{"bank": r["bank_name"], "reason": "FAILED_SOURCE_PARSING" if r["status"] == "FAILED" else r["status"]} for r in candidates if r not in verified]})
    AUDIT.write_text(json.dumps(audits, indent=2, ensure_ascii=False) + "\n")
    rank = {r["bank"]: r["rank"] for audit in audits for r in audit["banks"]}
    failure = {r["bank"]: r["reason"] for r in json.loads((ROOT / "data/fetch_failures.json").read_text()).get("failures", [])} if (ROOT / "data/fetch_failures.json").exists() else {}
    rows = []
    for r in snapshot["rows"]:
        special = next((p for p in r.get("products", []) if p.get("product_type") != "STANDARD_FD"), None) if r["status"] == "VERIFIED" else None
        cell = lambda value: html.escape(str(value if value not in (None, "") else "—"))
        current_rate = r.get("regular_rate") if r["status"] == "VERIFIED" else None
        rows.append(f'<tr><td>{cell(r["bank_name"])}</td><td>{cell(r["category"])}</td><td>{cell(r["status"])}</td><td>{cell(str(current_rate) + "%" if current_rate is not None else None)}</td><td>{cell((str(special["regular_rate"]) + "% " + special["product_name"]) if special else None)}</td><td>{cell("#" + str(rank[r["bank_name"]]) if r["bank_name"] in rank else None)}</td><td>{cell(failure.get(r["bank_name"]))}</td><td>{cell(r.get("verified_at"))}</td><td><a href="{html.escape(r.get("source_url", "#"))}">Official source</a></td></tr>')
    INVENTORY.write_text('<!doctype html><meta charset="utf-8"><title>All Banks - India FD Rates</title><h1>All Configured Banks</h1><p>Every registry entry is shown; only VERIFIED standard callable retail FDs enter the main ranking.</p><table border="1"><thead><tr><th>Bank</th><th>Category</th><th>Status</th><th>Standard Rate</th><th>Special Rate</th><th>Overall Rank</th><th>Failure Reason</th><th>Last Attempt</th><th>Source</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>\n')

if __name__ == "__main__": main()
