import re
from .base import TableParser, clean, result_from_rows
def parse(raw):
    text=clean(raw); marker=re.search(r"Key\s+Fixed\s+Deposit\s+Interest\s+Rates",text,re.I)
    if not marker: raise ValueError("Axis FD table marker not found")
    p=TableParser(); p.feed(text[marker.start():]); rows=[]
    for c in p.rows:
        if len(c)>=4 and re.search(r"day|month|year",c[0],re.I):
            nums=[float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", " | ".join(c))]
            if len(nums)>=4: rows.append((c[0],nums[0],nums[2],""))
    if not rows: raise ValueError("Axis domestic retail rows not found")
    return result_from_rows(rows)
