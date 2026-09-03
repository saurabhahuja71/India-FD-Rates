import re
from .base import TableParser, clean, result_from_rows
def parse(raw):
    text=clean(raw); marker=re.search(r"Revision\s+in\s+Interest\s+Rates\s+on\s+Retail",text,re.I)
    if not marker: raise ValueError("SBI retail revision table not found")
    p=TableParser(); p.feed(text[marker.start():]); rows=[]
    for c in p.rows:
        if len(c)>=5 and re.search(r"day|month|year",c[0],re.I):
            nums=[float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", " | ".join(c))]
            if len(nums)>=4: rows.append((c[0],nums[1],nums[3],""))
    if not rows: raise ValueError("SBI retail rate rows not found")
    return result_from_rows(rows)
