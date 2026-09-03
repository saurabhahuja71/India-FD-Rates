import re
from datetime import datetime
from .base import TableParser, clean, result_from_rows

CALLABLE_HEADING = "Fixed Deposits – Less than INR 3 crores – Premature Withdrawal Allowed"

def parse(raw):
    text = clean(raw)
    heading = re.search(r"Fixed\s+Deposits\s*[–-]\s*Less\s+than\s+INR\s+3\s+crores\s*[–-]\s*Premature\s+Withdrawal\s+Allowed", text, re.I)
    if not heading:
        raise ValueError("RBL callable below-INR-3-crore section not found")
    end = re.search(r"Fixed\s+Deposits\s*[–-]\s*Less\s+than\s+INR\s+3\s+crores\s*[–-]\s*Premature\s+Withdrawal\s+NOT\s+Allowed", text[heading.end():], re.I)
    block = text[heading.start():heading.end() + end.start()] if end else text[heading.start():]
    parser = TableParser(); parser.feed(block)
    header = next((r for r in parser.rows if any("Period of Deposit" in c for c in r)), None)
    if not header:
        raise ValueError("RBL callable table headers not found")
    header_pos = parser.rows.index(header)
    parent = parser.rows[header_pos - 1] if header_pos else []
    group_header = parent if any(re.search(r"General Citizen", c, re.I) for c in parent) else header
    if not any(re.search(r"General Citizen", c, re.I) for c in group_header) or not any(re.search(r"Senior Citizen", c, re.I) for c in group_header):
        raise ValueError("RBL callable table citizen group headers not found")
    def column(pattern):
        for i, value in enumerate(header):
            if re.search(pattern, value, re.I): return i
        raise ValueError(f"RBL required source column missing: {pattern}")
    period_i = column(r"Period of Deposit")
    regular_i = column(r"Interest Rates.*per annum")
    senior_i = next((i for i, value in enumerate(header) if i > regular_i and re.search(r"Interest Rates.*per annum", value, re.I)), None)
    if senior_i is None: raise ValueError("RBL senior citizen interest-rate column missing")
    # Both yield columns and Super Senior columns are deliberately ignored.
    rows=[]
    for cells in parser.rows:
        if len(cells) <= max(period_i, regular_i, senior_i): continue
        if not re.search(r"day|month|year", cells[period_i], re.I): continue
        regular = re.search(r"(\d+(?:\.\d+)?)\s*%", cells[regular_i])
        senior = re.search(r"(\d+(?:\.\d+)?)\s*%", cells[senior_i])
        if regular and senior:
            rows.append((cells[period_i], float(regular.group(1)), float(senior.group(1)), " | ".join(cells)))
    if not rows: raise ValueError("RBL callable retail rows not found")
    out = result_from_rows(rows)
    out.update({"callable": True, "customer_type": "RESIDENT_DOMESTIC_RETAIL_INDIVIDUAL",
                "source_table": CALLABLE_HEADING,
                "regular_source_column": f"General Citizen — {header[regular_i]}", "senior_source_column": f"Senior Citizen — {header[senior_i]}",
                "notes": "Callable retail table selected; effective annualised yield and Super Senior Citizen columns excluded."})
    m = re.search(r"Fixed\s+Deposits\s+w\.e\.f\.\s*([A-Za-z]+)\s*(\d{1,2})(?:st|nd|rd|th)?[,]?\s*(20\d{2})", block, re.I)
    if m:
        out["effective_date"] = datetime.strptime(f"{m.group(2)} {m.group(1)} {m.group(3)}", "%d %B %Y").date().isoformat()
    return out
