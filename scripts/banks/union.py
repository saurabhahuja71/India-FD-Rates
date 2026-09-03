import re
from .base import TableParser, clean, result_from_rows

def parse(raw):
    text = clean(raw)
    marker = re.search(r"Domestic/\s*NRO\s+Term\s+Deposit", text, re.I)
    if not marker:
        raise ValueError("Union Bank domestic retail section not found")
    start = text.rfind("<table", 0, marker.start())
    end = text.find("</table>", marker.start())
    parser = TableParser(); parser.feed(text[start:end + 8] if start >= 0 and end >= 0 else text[marker.start():])
    rows = []
    for cells in parser.rows:
        if len(cells) >= 2 and re.search(r"day|month|year", cells[0], re.I):
            rate = re.search(r"\d+(?:\.\d+)?", cells[1])
            if rate:
                regular = float(rate.group())
                rows.append((cells[0], regular, regular + 0.50, ""))
    if not rows:
        raise ValueError("Union Bank domestic retail rows not found")
    effective = re.search(r"effective\s+from\s+(\d{1,2}).*?([A-Za-z]+)\s+(20\d{2})", text[marker.start():marker.start() + 400], re.I)
    effective_date = None
    if effective:
        from datetime import datetime
        effective_date = datetime.strptime(" ".join(effective.groups()), "%d %B %Y").date().isoformat()
    result = result_from_rows(rows, effective_date=effective_date)
    result["notes"] = "Senior citizen rate is the official additional 0.50% benefit over the corresponding resident rate."
    return result
