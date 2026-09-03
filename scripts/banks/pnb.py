import re
from .base import TableParser, clean, result_from_rows

def parse(raw):
    text = clean(raw)
    marker = re.search(r"Revised\s+Rates\s+For\s+Public", text, re.I)
    if not marker:
        raise ValueError("PNB public retail rate table header not found")
    table_start = text.rfind("<table", 0, marker.start())
    table_end = text.find("</table>", marker.start())
    parser = TableParser(); parser.feed(text[table_start:table_end + 8] if table_start >= 0 and table_end >= 0 else text[marker.start():])
    rows = []
    for cells in parser.rows:
        if len(cells) >= 5 and re.search(r"day|month|year", cells[1], re.I):
            nums = []
            for value in cells[2:5]:
                match = re.search(r"\d+(?:\.\d+)?", value)
                nums.append(float(match.group()) if match else None)
            if nums[0] is not None and nums[1] is not None:
                rows.append((cells[1], nums[0], nums[1], ""))
    if not rows:
        raise ValueError("PNB domestic retail rows not found")
    effective = re.search(r"w\.e\.f\.\s*(\d{1,2}\.\d{1,2}\.20\d{2})", text[marker.start():marker.start() + 300], re.I)
    effective_date = None
    if effective:
        from datetime import datetime
        effective_date = datetime.strptime(effective.group(1), "%d.%m.%Y").date().isoformat()
    return result_from_rows(rows, effective_date=effective_date)
