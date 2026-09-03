import re
from .base import TableParser, clean, result_from_rows

def parse(raw):
    text = clean(raw)
    marker = re.search(r"BANK\s+HAS\s+REVISED\s+RATE.*?DOMESTIC\s*/\s*NRO.*?CALLABLE", text, re.I | re.S)
    if not marker:
        raise ValueError("BOI domestic/NRO callable retail section not found")
    start = text.find("<table", marker.start())
    end = text.find("</table>", start)
    parser = TableParser(); parser.feed(text[start:end + 8] if start >= 0 and end >= 0 else text[marker.start():])
    rows = []
    for cells in parser.rows:
        if len(cells) >= 2 and re.search(r"day|month|year", cells[0], re.I):
            rate = re.search(r"\d+(?:\.\d+)?", cells[1])
            if rate:
                rows.append((cells[0], float(rate.group()), None, ""))
    if not rows:
        raise ValueError("BOI domestic/NRO callable retail rows not found")
    # BOI publishes the senior benefit separately: +0.50% from 6 months to
    # under 3 years and +0.75% from 3 to 10 years.
    senior_rows = []
    for tenure, regular, _, _ in rows:
        bonus = 0.75 if re.search(r"3\s+Years|above\s+3|5\s+Years|8\s+years", tenure, re.I) else (0.50 if re.search(r"year|month", tenure, re.I) and not re.search(r"days", tenure, re.I) else 0.0)
        senior_rows.append((tenure, regular, regular + bonus, ""))
    result = result_from_rows(senior_rows)
    result["product_type"] = "STANDARD_FD"
    result["products"] = [{"product_name": "Domestic/NRO callable term deposit", "product_type": "STANDARD_FD", "regular_rate": result["regular_rate"], "senior_rate": result["senior_rate"], "tenure": result["regular_tenure"], "deposit_minimum": "₹10,000", "deposit_maximum": "Below ₹3 crore", "callable": True}, {"product_name": "Green Deposit / Harit Jama Yojana", "product_type": "GREEN_DEPOSIT", "regular_rate": 6.85, "senior_rate": 7.35, "tenure": "999 days", "deposit_minimum": "₹1 lakh", "deposit_maximum": "Below ₹10 crore", "callable": True}]
    result["notes"] = "Standard callable domestic/NRO retail FD. Green Deposit at 999 days is retained separately as GREEN_DEPOSIT and is not mixed into the standard ranking."
    return result
