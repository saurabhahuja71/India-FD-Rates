import re
from datetime import datetime
from .base import TableParser, clean, result_from_rows

def parse(raw):
    text = clean(raw)
    parser = TableParser(); parser.feed(text)
    header = next((r for r in parser.rows if r and re.search(r"domestic\s*/\s*nro\s*/\s*nre.*less than", " ".join(r), re.I)), None)
    if not header:
        raise ValueError("IDFC FIRST domestic retail rate table not found")
    start = parser.rows.index(header)
    rows = []
    for cells in parser.rows[start + 1:]:
        if not cells or re.search(r"tax saver|green deposit|bulk deposit", " ".join(cells), re.I):
            break
        if len(cells) >= 3 and re.search(r"day|year|month", cells[0], re.I):
            rates = [re.search(r"(\d+(?:\.\d+)?)", c) for c in cells[1:3]]
            if all(rates):
                rows.append((cells[0], float(rates[0].group(1)), float(rates[1].group(1)), " | ".join(cells)))
    if not rows:
        raise ValueError("IDFC FIRST eligible retail rate rows not found")
    out = result_from_rows(rows)
    out.update({
        "callable": True,
        "customer_type": "RESIDENT_DOMESTIC_RETAIL_INDIVIDUAL",
        "source_table": header[0],
        "regular_source_column": "General",
        "senior_source_column": "Senior Citizen",
        "notes": "Domestic/NRO/NRE retail table below ₹3 crore; NRI senior-citizen rates are excluded, while resident domestic senior rates are included.",
    })
    m = re.search(r"w\.e\.f\.\s*(\d{1,2})\s*(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(20\d{2})", header[0], re.I)
    if m:
        out["effective_date"] = datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%d %B %Y").date().isoformat()
    return out
