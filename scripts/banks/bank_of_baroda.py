import re
from .base import TableParser, clean, result_from_rows

def parse(raw):
    text = clean(raw)
    marker = re.search(r"Domestic\s+Term\s+Deposits.*?below.*?3\.00\s*Crores", text, re.I | re.S)
    if not marker:
        raise ValueError("Bank of Baroda domestic retail section not found")
    start = text.rfind("<table", 0, marker.start())
    end = text.find("</table>", marker.start())
    parser = TableParser(); parser.feed(text[start:end + 8] if start >= 0 and end >= 0 else text[marker.start():])
    rows = []
    for cells in parser.rows:
        if rows and not cells[0].strip():
            break
        if len(cells) >= 3 and re.search(r"day|month|year", cells[0], re.I):
            numbers = [re.search(r"\d+(?:\.\d+)?", cells[i]) for i in (1, 2)]
            if all(numbers):
                rows.append((cells[0], float(numbers[0].group()), float(numbers[1].group()), ""))
    if not rows:
        raise ValueError("Bank of Baroda domestic retail rows not found")
    effective = re.search(r"w\.e\.f\.?\s*(\d{1,2})[-./](\d{1,2})[-./](20\d{2})", text[marker.start():marker.start() + 300], re.I)
    effective_date = None
    if effective:
        from datetime import datetime
        effective_date = datetime.strptime("-".join(effective.groups()), "%d-%m-%Y").date().isoformat()
    result = result_from_rows(rows, effective_date=effective_date)
    result["notes"] = "Includes the bank's callable bob Golden Goal 555-day special deposit scheme; verify scheme terms before booking."
    return result
