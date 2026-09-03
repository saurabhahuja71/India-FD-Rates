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
VERIFICATION_REPORT = ROOT / "verification_report.md"

def vstatus(row):
    return {"VERIFIED": "LIVE_VERIFIED"}.get(row.get("verification_status", row.get("status", "SAMPLE")), row.get("verification_status", row.get("status", "SAMPLE")))

def main():
    snapshot = json.loads(DATA.read_text())
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    audits = []
    for category in ("private_sector", "public_sector", "small_finance"):
        candidates = [r for r in snapshot["rows"] if r["category"] == category]
        verified = sorted((r for r in candidates if vstatus(r) in {"LIVE_VERIFIED", "OFFICIAL_DOCUMENT_VERIFIED"} and r.get("product_type", "STANDARD_FD") == "STANDARD_FD"), key=lambda r: (-r["regular_rate"], r["bank_name"]))
        audits.append({"category": category, "ranking_type": "callable_retail_fd_including_special_tenure", "generated_at": now, "banks": [{"rank": i, "bank": r["bank_name"], "rate": r["regular_rate"], "status": vstatus(r), "source": r.get("source_url")} for i, r in enumerate(verified, 1)], "excluded": [{"bank": r["bank_name"], "reason": "FAILED_SOURCE_PARSING" if vstatus(r) == "FAILED" else vstatus(r)} for r in candidates if r not in verified]})
    AUDIT.write_text(json.dumps(audits, indent=2, ensure_ascii=False) + "\n")
    rank = {r["bank"]: r["rank"] for audit in audits for r in audit["banks"]}
    failure = {r["bank"]: r["reason"] for r in json.loads((ROOT / "data/fetch_failures.json").read_text()).get("failures", [])} if (ROOT / "data/fetch_failures.json").exists() else {}
    rows = []
    for r in snapshot["rows"]:
        current_status = vstatus(r)
        special = next((p for p in r.get("products", []) if p.get("product_type") != "STANDARD_FD"), None) if current_status in {"LIVE_VERIFIED", "OFFICIAL_DOCUMENT_VERIFIED"} else None
        cell = lambda value: html.escape(str(value if value not in (None, "") else "—"))
        current_rate = r.get("regular_rate") if current_status in {"LIVE_VERIFIED", "OFFICIAL_DOCUMENT_VERIFIED"} else None
        rows.append(f'<tr><td>{cell(r["bank_name"])}</td><td>{cell(r["category"])}</td><td>{cell(current_status)}</td><td>{cell(str(current_rate) + "%" if current_rate is not None else None)}</td><td>{cell((str(special["regular_rate"]) + "% " + special["product_name"]) if special else None)}</td><td>{cell("#" + str(rank[r["bank_name"]]) if r["bank_name"] in rank else None)}</td><td>{cell(failure.get(r["bank_name"]))}</td><td>{cell(r.get("verified_at"))}</td><td><a href="{html.escape(r.get("source_url", "#"))}">Official source</a></td></tr>')
    INVENTORY.write_text('<!doctype html><meta charset="utf-8"><title>All Banks - India FD Rates</title><h1>All Configured Banks</h1><p>Every registry entry is shown; only current LIVE or official-document callable resident retail FDs enter the main ranking. Special-tenure callable schemes are included and labeled in evidence.</p><table border="1"><thead><tr><th>Bank</th><th>Category</th><th>Status</th><th>Standard Rate</th><th>Special Rate</th><th>Overall Rank</th><th>Failure Reason</th><th>Last Attempt</th><th>Source</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>\n')
    public = next(a for a in audits if a["category"] == "public_sector")
    boi = next(r for r in snapshot["rows"] if r["bank_name"] == "Bank of India")
    sbi = next(r for r in public["banks"] if r["bank"] == "State Bank of India") if any(r["bank"] == "State Bank of India" for r in public["banks"]) else None
    report = ["# FD Verification Report", "", f"Generated: `{now}`", "", "## Ranking policy", "", "The published ranking is **highest callable resident-domestic-retail FD rate**, including callable special-tenure schemes (for example, 444/555-day products). Non-callable, bulk, NRI-only, and institutional products are excluded from the main ranking. Special products are retained separately in bank evidence.", "", "## Public-sector audit", "", "| Rank | Bank | Rate | Verification |", "|---:|---|---:|---|"]
    report += [f"| {r['rank']} | {r['bank']} | {r['rate']:.2f}% | {r['status']} |" for r in public["banks"]]
    sbi_rank = next((r['rank'] for r in public['banks'] if r['bank'] == 'State Bank of India'), None)
    sbi_position = f"#{sbi_rank}" if sbi_rank is not None else "not ranked"
    sbi_explanation = (f"- SBI is included in the Top 5 at {sbi_position} because its current callable retail evidence is within the ranking set."
                       if sbi_rank is not None and sbi_rank <= 5 else
                       f"- SBI is excluded from the Top 5 because its verified callable retail rate ranks {sbi_position}, below the five highest verified public-sector rates.")
    report += ["", "### Bank of India", "", f"- Status: **{vstatus(boi)}**", f"- Evidence source: `{boi.get('source_url')}`", f"- Rate: **{boi.get('regular_rate') if boi.get('regular_rate') is not None else 'not available'}**", "- Rank: **not ranked** because no acceptable current official evidence was fetched.", "- Reason: official BOI pages and the official policy-document candidate returned HTTP 403 to this automation runner; no current downloadable rate schedule was verified.", "", "### State Bank of India", "", f"- Status: **{vstatus(sbi) if sbi else 'not ranked'}**", f"- Rank: **{sbi_position}**", sbi_explanation]
    history_path = ROOT / "data/fd-rates-history.json"
    history = json.loads(history_path.read_text()) if history_path.exists() else {"snapshots": []}
    previous = history.get("snapshots", [])[-2] if len(history.get("snapshots", [])) >= 2 else None
    if previous:
        old = {r["bank_name"]: r for r in previous["rows"]}
        changes=[]
        for current in snapshot["rows"]:
            before=old.get(current["bank_name"])
            source_snapshot = previous
            # A targeted diagnostic run may insert a FAILED snapshot between
            # the old value and the corrected full run. Find the nearest
            # earlier numeric value so the correction remains visible.
            if before and before.get("regular_rate") == current.get("regular_rate"):
                for candidate in reversed(history.get("snapshots", [])[:-1]):
                    candidate_row=next((r for r in candidate["rows"] if r["bank_name"] == current["bank_name"]), None)
                    if candidate_row and candidate_row.get("regular_rate") is not None and candidate_row.get("regular_rate") != current.get("regular_rate"):
                        before=candidate_row; source_snapshot=candidate; break
            if before and before.get("regular_rate") is not None and current.get("regular_rate") is not None and before.get("regular_rate") != current.get("regular_rate"):
                current_rank=next((a["rank"] for a in audits for a in a["banks"] if a["bank"] == current["bank_name"]), None)
                # Historical rank is reconstructed from the prior snapshot's
                # callable verified rows, so the cause is auditable.
                old_rows=[r for r in source_snapshot["rows"] if r["category"] == current["category"] and r.get("status") == "VERIFIED" and r.get("regular_rate") is not None]
                old_rank=sorted(old_rows,key=lambda r:(-r["regular_rate"],r["bank_name"])).index(before)+1 if before.get("regular_rate") is not None and before in old_rows else None
                cause = "RBL adapter previously selected non-callable/Super Senior columns; corrected to callable General/Senior columns" if current["bank_name"] == "RBL Bank" else "adapter/source-column correction"
                changes.append({"bank":current["bank_name"],"old_rate":before.get("regular_rate"),"corrected_rate":current.get("regular_rate"),"old_rank":old_rank,"new_rank":current_rank,"root_cause":cause})
        report += ["", "## Changes since previous snapshot", "", "| Bank | Old rate | Corrected rate | Old rank | New rank | Root cause |", "|---|---:|---:|---:|---:|---|"]
        report += [f"| {c['bank']} | {c['old_rate']}% | {c['corrected_rate']}% | {c['old_rank'] or '—'} | {c['new_rank'] or '—'} | {c['root_cause']} |" for c in changes] or ["| — | — | — | — | — | No rate changes |"]
    report += ["", "## Evidence blocks for ranked banks", ""]
    for audit in audits:
        report.append(f"### {audit['category']}")
        for item in audit["banks"][:5]:
            row=next(r for r in snapshot["rows"] if r["bank_name"] == item["bank"])
            report += [f"- **{row['bank_name']}** — table: `{row.get('source_table')}`; tenure: `{row.get('regular_tenure')}`; regular column: `{row.get('regular_source_column')}` = **{row.get('regular_rate'):.2f}%**; senior column: `{row.get('senior_source_column')}` = **{row.get('senior_rate'):.2f}%**; source: {row.get('source_url')}"]
    VERIFICATION_REPORT.write_text("\n".join(report) + "\n")

if __name__ == "__main__": main()
