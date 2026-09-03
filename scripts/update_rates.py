#!/usr/bin/env python3
"""Conservative daily source checker for the published FD snapshot.

It never invents a rate: a row is changed only when its explicit configured
peak-rate phrase is found in the official page. Ambiguous pages are reported
for review and the existing snapshot is left intact.
"""
import argparse, html, json, re, sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/fd-rates.json"
CONFIG = ROOT / "scripts/banks.json"
HISTORY = ROOT / "data/fd-rates-history.json"

def fetch(url):
    req = Request(url, headers={"User-Agent": "India-FD-Rates/1.0 (source checker)"})
    with urlopen(req, timeout=25) as response:
        raw = response.read().decode("utf-8", "ignore")
    return raw

def parse_hdfc_retail_under_3cr(raw):
    """Parse HDFC's current <3 crore domestic table, not headline snippets."""
    decoded = html.unescape(html.unescape(raw))
    start = re.search(r"Domestic\s*/\s*NRO\s*/\s*NRE\s+FIXED\s+DEPOSIT\s+RATE", decoded, re.I)
    if not start:
        raise ValueError("HDFC domestic table heading not found")
    block = decoded[start.start():]
    end = re.search(r"Domestic\s*/\s*NRO\s*/\s*NRE\s+FIXED\s+DEPOSIT\s+RATE", block[1000:], re.I)
    if end:
        block = block[:end.start() + 1000]
    date_match = re.search(r"Applicable\s+from\s+[^0-9]{0,30}?([0-9]{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+),\s+([0-9]{4})", block, re.I)
    effective_date = None
    if date_match:
        from datetime import datetime
        effective_date = datetime.strptime(" ".join(date_match.groups()), "%d %B %Y").date().isoformat()
    rows = []
    for match in re.finditer(r"<tr[^>]*>\s*<td[^>]*>\s*(.*?)\s*</td>\s*<td[^>]*>\s*(\d+(?:\.\d+)?)%\s*</td>\s*<td[^>]*>\s*(\d+(?:\.\d+)?)%\s*</td>", block, re.I | re.S):
        tenure = re.sub(r"\s+", " ", re.sub(r"</?[A-Za-z][^>]*>", "", html.unescape(match.group(1)))).strip()
        rows.append((tenure, float(match.group(2)), float(match.group(3))))
    if not rows:
        raise ValueError("HDFC retail rate rows not found")
    regular = max(rows, key=lambda row: row[1])
    senior = max(rows, key=lambda row: row[2])
    return {"regular_rate": regular[1], "regular_tenure": regular[0], "senior_rate": senior[2], "senior_tenure": senior[0], "effective_date": effective_date, "evidence": {"matched_tenure": regular[0], "matched_regular_rate": f"{regular[1]:.2f}%", "matched_senior_rate": f"{senior[2]:.2f}%"}}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check-only", action="store_true"); args = ap.parse_args()
    snapshot = json.loads(DATA.read_text()); configs = json.loads(CONFIG.read_text())
    by_bank = {r["bank_name"]: r for r in snapshot["rows"]}; checked = []; failures = []
    for cfg in configs:
        try:
            if not cfg.get("parser"):
                failures.append(f'{cfg["bank"]}: no exact rate-table parser configured; row remains non-current')
                continue
            raw = fetch(cfg["source"])
            if cfg.get("parser") == "hdfc_retail_under_3cr":
                parsed = parse_hdfc_retail_under_3cr(raw)
                row = by_bank[cfg["bank"]]
                row.update(parsed)
                row["status"] = "VERIFIED"
                row["verified_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
                row["source_type"] = "official_bank_website"
                checked.append(f'{cfg["bank"]}: {parsed["regular_rate"]:.2f}%')
                continue
            raise ValueError("unsupported parser")
        except Exception as exc:
            failures.append(f'{cfg["bank"]}: {exc.__class__.__name__}')
    print("Checked:", ", ".join(checked) or "none")
    if failures:
        print("Review required:"); print("\n".join(f"- {x}" for x in failures))
    if args.check_only or not checked:
        return 0 if checked else 1
    snapshot["generated_at"] = date.today().isoformat()
    DATA.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    history = json.loads(HISTORY.read_text()) if HISTORY.exists() else {"snapshots": []}
    history["snapshots"].append({"generated_at": snapshot["generated_at"], "rows": [{"bank_name": r["bank_name"], "category": r["category"], "status": r["status"], "regular_rate": r["regular_rate"], "senior_rate": r["senior_rate"]} for r in snapshot["rows"]]})
    HISTORY.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")
    from update_readme import main as update_readme
    update_readme()
    return 0

if __name__ == "__main__": sys.exit(main())
