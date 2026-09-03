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

def build_tables(snapshot):
    sections = [
        ("private_sector", "🏦 Top 5 Private Sector Banks"),
        ("public_sector", "🏛️ Top 5 Public Sector Banks"),
        ("small_finance", "🏦 Top 5 Small Finance Banks"),
    ]
    output = []
    for category, title in sections:
        rows = sorted((r for r in snapshot["rows"] if r["category"] == category and r["status"] == "VERIFIED"), key=lambda r: (-r["regular_rate"], r["bank_name"]))[:5]
        output += [f"## {title}", "", "| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |", "|------|------|-----------------|----------------|--------|---------------|--------|"]
        for rank, row in enumerate(rows, 1):
            regular = f'{row["regular_rate"]:.2f}%'; senior = f'{row["senior_rate"]:.2f}%'
            tenure = row["regular_tenure"] if row["regular_tenure"] == row["senior_tenure"] else f'Regular: {row["regular_tenure"]}<br>Senior: {row["senior_tenure"]}'
            notes = f' — {row["notes"]}' if row.get("notes") else ""
            output.append(f'| {rank} | {row["bank_name"]}{notes} | {regular} | {senior} | {tenure} | {fmt_date(row["verified_at"][:10])} | [Official]({row["source_url"]}) |')
        if not rows:
            output.append("| — | No VERIFIED retail rate available | — | — | — | — | — |")
        output.append("")
    output += ["### Last Updated", "", f'`{fmt_date(snapshot["generated_at"])} · source snapshot`', "", "> ⚠️ FD rates change frequently. Always verify the rate, tenure, eligibility and conditions on the official bank website before investing."]
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
