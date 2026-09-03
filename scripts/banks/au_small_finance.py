import re
from .base import TableParser, clean, result_from_rows
def parse(raw):
    text=clean(raw); start=re.search(r"Domestic,\s*NRE.*?Retail\s+Fixed\s+Deposit\s+Interest\s+Rates",text,re.I)
    senior=re.search(r"Senior\s+Citizen\s+Fixed\s+Deposit\s+Interest\s+Rates",text,re.I)
    if not start or not senior: raise ValueError("AU retail tables not found")
    def table(block):
        p=TableParser(); p.feed(block); out=[]
        for c in p.rows:
            if len(c)>=2 and re.search(r"day|month|year",c[0],re.I):
                nums=[float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", " | ".join(c))]
                if nums: out.append((c[0],nums[0]))
        return out
    regular_block=text[start.start():senior.start()]
    noncallable=re.search(r"Non-callable",regular_block,re.I)
    if noncallable: regular_block=regular_block[:noncallable.start()]
    senior_block=text[senior.start():]
    next_section=re.search(r"For\s+Domestic,\s*NRE",senior_block[500:],re.I)
    if next_section: senior_block=senior_block[:next_section.start()+500]
    regular=table(regular_block); senior_rows=table(senior_block)
    senior_by={t:s for t,s in senior_rows}; combined=[(t,r,senior_by[t],"") for t,r in regular if t in senior_by]
    if not combined: raise ValueError("AU matching regular/senior retail rows not found")
    return result_from_rows(combined)
