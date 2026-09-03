#!/usr/bin/env python3
"""Regenerate only the marked FD tables section in README.md."""
import json
from datetime import datetime, timezone
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
        ("private", "🏦 Top 5 Private Sector Banks"),
        ("public", "🏛️ Top 5 Public Sector Banks"),
        ("small-finance", "🏦 Top 5 Small Finance Banks"),
    ]
    output = []
    for category, title in sections:
        rows = sorted((r for r in snapshot["rows"] if r["category"] == category), key=lambda r: (-r["regular"]["rate"], r["bank"]))[:5]
        output += [f"## {title}", "", "| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |", "|------|------|-----------------|----------------|--------|---------------|--------|"]
        for rank, row in enumerate(rows, 1):
            regular = f'{row["regular"]["rate"]:.2f}%'
            senior = f'{row["senior"]["rate"]:.2f}%'
            tenure = row["regular"]["tenure"] if row["regular"]["tenure"] == row["senior"]["tenure"] else f'Regular: {row["regular"]["tenure"]}<br>Senior: {row["senior"]["tenure"]}'
            notes = f' — {row["notes"]}' if row.get("notes") else ""
            output.append(f'| {rank} | {row["bank"]}{notes} | {regular} | {senior} | {tenure} | {fmt_date(row["last_updated"])} | [Official]({row["source"]}) |')
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
