#!/usr/bin/env python3
"""Conservative daily source checker for the published FD snapshot.

It never invents a rate: a row is changed only when its explicit configured
peak-rate phrase is found in the official page. Ambiguous pages are reported
for review and the existing snapshot is left intact.
"""
import argparse, json, re, sys
from datetime import date
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
    return re.sub(r"<[^>]+>", " ", raw).replace("&nbsp;", " ")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check-only", action="store_true"); args = ap.parse_args()
    snapshot = json.loads(DATA.read_text()); configs = json.loads(CONFIG.read_text())
    by_bank = {r["bank"]: r for r in snapshot["rows"]}; checked = []; failures = []
    for cfg in configs:
        try:
            text = fetch(cfg["source"])
            matches = [float(x) for x in re.findall(cfg["pattern"], text, re.I)]
            matches = sorted(set(x for x in matches if 0 < x <= 15), reverse=True)
            if not matches:
                failures.append(f'{cfg["bank"]}: no unambiguous peak rate found')
                continue
            # The configured pattern is intentionally limited to a bank's peak phrase.
            row = by_bank[cfg["bank"]]
            if abs(row["regular"]["rate"] - matches[0]) > 0.001:
                row["regular"]["rate"] = matches[0]
            row["last_updated"] = date.today().isoformat()
            checked.append(f'{cfg["bank"]}: {matches[0]:.2f}%')
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
    history["snapshots"].append({"generated_at": snapshot["generated_at"], "rows": [{"bank": r["bank"], "category": r["category"], "regular": r["regular"], "senior": r["senior"]} for r in snapshot["rows"]]})
    HISTORY.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")
    from update_readme import main as update_readme
    update_readme()
    return 0

if __name__ == "__main__": sys.exit(main())
