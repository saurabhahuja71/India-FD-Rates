#!/usr/bin/env python3
"""Regenerate only the marked FD tables section in README.md."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/fd-rates.json"
README = ROOT / "README.md"
START = "<!-- FD_TABLES_START -->"
END = "<!-- FD_TABLES_END -->"

def fmt_date(value):
    return datetime.strptime(value, "%Y-%m-%d").strftime("%d %b %Y")

def vstatus(row):
    return {"VERIFIED": "LIVE_VERIFIED"}.get(row.get("verification_status", row.get("status", "SAMPLE")), row.get("verification_status", row.get("status", "SAMPLE")))

def build_tables(snapshot):
    sections = [
        ("private_sector", "🏦 Highest Callable Retail FD Rates — Private Sector"),
        ("public_sector", "🏛️ Highest Callable Retail FD Rates — Public Sector"),
        ("small_finance", "🏦 Highest Callable Retail FD Rates — Small Finance"),
    ]
    output = []
    for category, title in sections:
        rows = sorted((r for r in snapshot["rows"] if r["category"] == category and vstatus(r) in {"LIVE_VERIFIED", "OFFICIAL_DOCUMENT_VERIFIED"}), key=lambda r: (-r["regular_rate"], r["bank_name"]))[:5]
        output += [f"## {title}", "", "| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Verification | Last Verified | Source |", "|------|------|-----------------|----------------|--------|--------------|---------------|--------|"]
        for rank, row in enumerate(rows, 1):
            regular = f'{row["regular_rate"]:.2f}%'; senior = f'{row["senior_rate"]:.2f}%'
            tenure = row["regular_tenure"] if row["regular_tenure"] == row["senior_tenure"] else f'Regular: {row["regular_tenure"]}<br>Senior: {row["senior_tenure"]}'
            label = "LIVE" if vstatus(row) == "LIVE_VERIFIED" else "DOCUMENT"
            output.append(f'| {rank} | {row["bank_name"]} | {regular} | {senior} | {tenure} | {label} | {fmt_date(row["verified_at"][:10])} | [Official]({row["source_url"]}) |')
        if not rows:
            output.append("| — | No eligible current retail rate available | — | — | — | — | — | — |")
        elif len(rows) < 5:
            output.append("")
            output.append(f"> ⚠️ Only {len(rows)} bank(s) could be verified in the latest collection run.")
        output.append("")
    output += ["## Data Coverage", ""]
    for category, label in [("private_sector", "Private Sector"), ("public_sector", "Public Sector"), ("small_finance", "Small Finance")]:
        total = sum(r["category"] == category for r in snapshot["rows"]); verified = sum(r["category"] == category and vstatus(r) in {"LIVE_VERIFIED", "OFFICIAL_DOCUMENT_VERIFIED"} for r in snapshot["rows"])
        output.append(f"- **{label}:** ✅ {verified} / {total} banks verified")
    output += ["", "### Last Collection Run", "", f'`{fmt_date(snapshot["generated_at"])} · source snapshot`', "", "> ⚠️ FD rates change frequently. Always verify the rate, tenure, eligibility and conditions on the official bank website before investing."]
    return "\n".join(output)

def main():
    snapshot = json.loads(DATA.read_text())
    readme = README.read_text()
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) > readme.index(END):
        raise SystemExit("README must contain exactly one valid FD table marker pair")
    start = readme.index(START) + len(START)
    end = readme.index(END)
    README.write_text(readme[:start] + "\n\n" + build_tables(snapshot) + "\n\n" + readme[end:])

if __name__ == "__main__": main()
