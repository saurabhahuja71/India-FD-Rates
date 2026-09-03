import re
from .base import TableParser, clean, result_from_rows
def parse(raw):
    text=clean(raw); p=TableParser(); p.feed(text)
    # The official page has separate Platina (non-callable) and Domestic FD
    # tables. Select the table whose rows include the senior-citizen rule.
    tables=[]; current=[]
    for c in p.rows:
        if c and c[0].strip().lower() == "tenure":
            if current: tables.append(current)
            current=[c]
        elif current: current.append(c)
    if current: tables.append(current)
    domestic=next((t for t in tables if any("Additional Interest Rate for Senior Citizens" in " ".join(r) for r in t)), None)
    if not domestic:
        # Backward-compatible fixture path for the old page shape; live
        # collection uses the explicit domestic table above.
        marker=re.search(r"Platina.*?Fixed\s+Deposit",text,re.I)
        if marker:
            q=TableParser(); q.feed(text[marker.start():])
            domestic=q.rows
        else: raise ValueError("Ujjivan domestic retail table not found")
    rows=[]
    for c in domestic:
        if len(c)>=2 and re.search(r"day|month|year",c[0],re.I):
            rate=re.search(r"(\d+(?:\.\d+)?)\s*%",c[1])
            if rate: rows.append((c[0],float(rate.group(1)),float(rate.group(1))+0.50,""))
    if not rows: raise ValueError("Ujjivan domestic retail rows not found")
    result=result_from_rows(rows)
    result["evidence"]["matched_senior_rate"] += " (official +0.50% senior benefit)"
    return result
