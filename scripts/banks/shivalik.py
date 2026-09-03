import re
from datetime import datetime
from .base import TableParser, clean, result_from_rows

def parse(raw):
    text=clean(raw); p=TableParser(); p.feed(text)
    tables=[]; current=[]
    for c in p.rows:
        if c and c[0].strip().lower() in {"tenure bucket", "tenure"}:
            if current: tables.append(current)
            current=[c]
        elif current: current.append(c)
    if current: tables.append(current)
    table=next((t for t in tables if any("7 days to 14 days" in " ".join(r) for r in t)), None)
    if not table: raise ValueError("Shivalik callable domestic FD table not found")
    rows=[]
    for c in table:
        if len(c)>=3 and re.search(r"day|month|year",c[0],re.I):
            vals=[re.search(r"(\d+(?:\.\d+)?)\s*%",x) for x in c[1:3]]
            if all(vals): rows.append((c[0],float(vals[0].group(1)),float(vals[1].group(1))," | ".join(c)))
    if not rows: raise ValueError("Shivalik callable domestic FD rows not found")
    out=result_from_rows(rows)
    section=text.find("Fixed Deposits Rates")
    m=re.search(r"w\.e\.f\.\s*([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?[, ]+\s*(20\d{2})",text[section:] if section >= 0 else text,re.I)
    if m: out["effective_date"] = datetime.strptime(f"{m.group(2)} {m.group(1)} {m.group(3)}","%d %B %Y").date().isoformat()
    out["notes"]="Callable domestic retail FD below ₹3 crore; non-callable table is retained as a separate product by the source but excluded from the main ranking."
    return out
