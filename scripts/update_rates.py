#!/usr/bin/env python3
"""Collect official retail FD tables through independent bank adapters."""
import argparse, html, importlib, json, re, sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA, HISTORY, CONFIG = ROOT / "data/fd-rates.json", ROOT / "data/fd-rates-history.json", ROOT / "config/banks.yaml"
FAILURES = ROOT / "data/fetch_failures.json"
VALID_STATUSES = {"VERIFIED", "STALE", "FAILED", "SAMPLE"}

def load_config():
    try:
        import yaml
        return yaml.safe_load(CONFIG.read_text())["banks"]
    except ImportError as exc:
        raise SystemExit("PyYAML is required: python -m pip install pyyaml") from exc

def fetch(source):
    req = Request(source["url"], headers={"User-Agent": "India-FD-Rates/1.0 official-source-checker"})
    with urlopen(req, timeout=8) as response:
        raw = response.read()
        return {"raw": raw, "content_type": response.headers.get_content_type(),
                "status": response.status, "final_url": response.geturl()}

def effective_from(raw):
    text = html.unescape(html.unescape(raw.decode("utf-8", "ignore")))
    text = re.sub(r"</?[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    match = re.search(r"(?:Applicable|Effective)\s+(?:from|date)\s*[^0-9]{0,40}?([0-9]{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)[, ]+([0-9]{4})", text, re.I)
    if not match:
        match = re.search(r"(?:w\.e\.f\.?|with effect from)\s*[^0-9]{0,10}([0-9]{1,2})[./-]([0-9]{1,2})[./-](20\d{2})", text, re.I)
    if not match: return None
    try:
        value = " ".join(match.groups())
        for fmt in ("%d %B %Y", "%d %m %Y"):
            try: return datetime.strptime(value, fmt).date().isoformat()
            except ValueError: pass
    except ValueError: pass
    return None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--bank"); ap.add_argument("--verbose", action="store_true"); args = ap.parse_args()
    snapshot = json.loads(DATA.read_text()); configs = load_config(); by_bank = {r["bank_name"]: r for r in snapshot["rows"]}
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"); checked=[]; failures=[]
    for cfg in configs:
        if not cfg.get("enabled", True): continue
        row = by_bank.get(cfg["name"])
        if not row: failures.append(f'{cfg["name"]}: missing data row'); continue
        row.update({"category": cfg["category"], "deposit_category": cfg["deposit_category"], "deposit_limit": cfg["retail_threshold"], "source_url": cfg["official_sources"][0]["url"]})
        if args.bank and cfg["id"] != args.bank: continue
        if not cfg.get("parser"):
            failures.append(f'{cfg["name"]}: no exact rate-table adapter configured; row remains non-current')
            continue
        attempts = []
        failure_stage = "source_fetch"
        try:
            parsed = None; source_used = None; source_meta = None
            for source in cfg["official_sources"]:
                try:
                    meta = fetch(source); raw = meta["raw"]
                    is_pdf = source["type"] == "pdf" or meta["content_type"] == "application/pdf" or raw[:4] == b"%PDF"
                    table_count = None
                    if not is_pdf:
                        from banks.base import TableParser
                        parser = TableParser(); parser.feed(raw.decode("utf-8", "ignore")); table_count = len(parser.rows)
                    meta.update({"url": source["url"], "type": source["type"], "format": "PDF" if is_pdf else "HTML", "table_count": table_count})
                    attempts.append(meta | {"raw": None})
                    if args.verbose: print(f'[{cfg["id"]}] source={source["url"]} type={source["type"]} http={meta["status"]} final={meta["final_url"]} content_type={meta["content_type"]} format={meta["format"]} tables={table_count if table_count is not None else "n/a"}')
                    module = importlib.import_module(f'banks.{cfg["parser"]}')
                    failure_stage = "retail_section_detection"
                    parsed = module.parse(raw)
                    failure_stage = "validation"
                    source_used, source_meta = source, meta
                    break
                except Exception as exc:
                    if not attempts or attempts[-1].get("url") != source["url"]:
                        attempts.append({"url": source["url"], "type": source["type"]})
                    attempts[-1]["error"] = str(exc)
                    if args.verbose: print(f'[{cfg["id"]}] source failed: {exc}')
            if not parsed:
                raise ValueError("all official sources failed")
            row.update(parsed); row.update({"status":"VERIFIED", "verified_at":now, "source_url":source_used["url"], "source_type":"official_endpoint" if source_used["type"] == "endpoint" else ("official_pdf" if source_used["type"] == "pdf" else "official_bank_website")})
            if not row.get("effective_date"): row["effective_date"] = effective_from(raw)
            if not row.get("effective_date"): row["effective_date_note"] = "Official page did not publish an effective date; verified at retrieval time."
            if args.verbose: print(f'[{cfg["id"]}] effective={row["effective_date"]} rows={row.get("row_count", "?")} retail_rows={row.get("row_count", "?")} regular={row["regular_rate"]:.2f}% @ {row["regular_tenure"]} senior={row["senior_rate"]:.2f}% @ {row["senior_tenure"]} VALIDATED')
            checked.append(cfg["name"])
        except Exception as exc:
            row["status"] = "FAILED"; row["verified_at"] = None; row["effective_date"] = None; row["evidence"] = {"matched_tenure":None,"matched_regular_rate":None,"matched_senior_rate":None}; failures.append(f'{cfg["name"]}: {exc}')
            failures[-1] = {"bank": cfg["name"], "attempted_sources": attempts, "failure_stage": failure_stage, "reason": str(exc), "last_http_status": attempts[-1].get("status") if attempts else None, "validation_rule": "official source, retail section, explicit tenure and regular/senior rate required"}
            if args.verbose: print(f'[{cfg["id"]}] FAILED: {exc}')
    print(f"Verified {len(checked)} bank(s); failed {len(failures)}")
    if failures and not args.verbose:
        print("\n".join(f'- {x["bank"]}: {x["reason"]}' if isinstance(x, dict) else f"- {x}" for x in failures))
    snapshot["generated_at"] = date.today().isoformat(); DATA.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    FAILURES.write_text(json.dumps({"generated_at": now, "failures": failures}, indent=2, ensure_ascii=False) + "\n")
    history = json.loads(HISTORY.read_text()) if HISTORY.exists() else {"snapshots":[]}
    history["snapshots"].append({"generated_at":snapshot["generated_at"],"rows":[{"bank_name":r["bank_name"],"category":r["category"],"status":r["status"],"regular_rate":r["regular_rate"],"senior_rate":r["senior_rate"]} for r in snapshot["rows"]]})
    HISTORY.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")
    from update_readme import main as update_readme
    update_readme()
    return 0 if checked else 1

if __name__ == "__main__": sys.exit(main())
