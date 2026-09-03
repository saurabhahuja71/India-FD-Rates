import re
from .base import TableParser, clean, result_from_rows
def parse(raw):
    text=clean(raw); marker=re.search(r"Platina.*?Fixed\s+Deposit",text,re.I)
    if not marker: raise ValueError("Ujjivan domestic retail table not found")
    p=TableParser(); p.feed(text[marker.start():]); rows=[]
    for c in p.rows:
        if len(c)>=2 and re.search(r"day|month|year",c[0],re.I):
            rate=re.search(r"(\d+(?:\.\d+)?)\s*%",c[1])
            if rate: rows.append((c[0],float(rate.group(1)),float(rate.group(1))+0.50,""))
    if not rows: raise ValueError("Ujjivan domestic retail rows not found")
    result=result_from_rows(rows)
    result["evidence"]["matched_senior_rate"] += " (official +0.50% senior benefit)"
    return result
