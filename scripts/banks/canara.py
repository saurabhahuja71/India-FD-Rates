import re
from .base import TableParser, clean, result_from_rows

def parse(raw):
    text = clean(raw)
    marker = re.search(r"2\.\s*TERM\s+DEPOSITS.*?Deposits\s+less\s+than\s+Rs\.3\s+Crore", text, re.I | re.S)
    if not marker:
        marker = re.search(r"TERM\s+DEPOSITS.*?Rate\s+of\s+Interest.*?less\s+than\s+Rs\.3\s+Crore", text, re.I | re.S)
    if not marker:
        raise ValueError("Canara domestic retail term-deposit section not found")
    parser = TableParser(); parser.feed(text[marker.start():])
    rows = []
    for cells in parser.rows:
        if len(cells) >= 5 and re.search(r"day|month|year", cells[0], re.I):
            # Callable columns: General Public and Senior Citizen. Ignore
            # annualised yield and the non-callable (above Rs.1 crore) slab.
            values = [re.search(r"\d+(?:\.\d+)?", cells[i]) for i in (1, 3)]
            if all(values):
                rows.append((cells[0], float(values[0].group()), float(values[1].group()), ""))
    if not rows:
        raise ValueError("Canara domestic retail rows not found")
    effective = re.search(r"w\.e\.f\.\s*(\d{1,2}\.\d{1,2}\.20\d{2})", text[marker.start():marker.start() + 300], re.I)
    effective_date = None
    if effective:
        from datetime import datetime
        effective_date = datetime.strptime(effective.group(1), "%d.%m.%Y").date().isoformat()
    result = result_from_rows(rows, effective_date=effective_date)
    result["notes"] = "Callable domestic deposit; 444/555-day starred rates have the bank's stated minimum-deposit condition."
    return result
