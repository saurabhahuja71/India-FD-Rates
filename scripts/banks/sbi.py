import re
from .base import TableParser, clean, result_from_rows
def parse(raw):
    text=clean(raw); marker=re.search(r"Retail\s+Domestic\s+term\s+deposits",text,re.I)
    if not marker: raise ValueError("SBI retail domestic term-deposit section not found")
    p=TableParser(); p.feed(text[marker.start():]); rows=[]
    for c in p.rows:
        if len(c)>=5 and re.search(r"day|month|year",c[0],re.I):
            nums=[float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%?", " | ".join(c[1:5]))]
            if len(nums)>=4: rows.append((c[0],nums[0],nums[2],""))
    if not rows: raise ValueError("SBI retail rate rows not found")
    return result_from_rows(rows)
