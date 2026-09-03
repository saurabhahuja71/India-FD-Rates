import re
from datetime import datetime
from .base import TableParser, clean, result_from_rows

def parse(raw):
    p=TableParser(); p.feed(clean(raw))
    rows=[]; found=False
    for c in p.rows:
        if len(c)>=3 and c[0].strip().lower() == "tenure" and not found:
            found=True; continue
        if found and len(c)>=3 and re.search(r"day|month|year",c[0],re.I):
            nums=[]
            for value in c[1:3]:
                m=re.search(r"(\d+(?:\.\d+)?)",value)
                if m: nums.append(float(m.group(1)))
            if len(nums)==2: rows.append((c[0],nums[0],nums[1]," | ".join(c)))
        if found and c and "Senior Citizens - Additional" in c[0]: break
    if not rows: raise ValueError("IndusInd domestic callable retail table not found")
    out=result_from_rows(rows)
    m=re.search(r"w\.e\.f\.\s*(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)[’']?(\d{2,4})",clean(raw),re.I)
    if m:
        year=int(m.group(3)); year += 2000 if year < 100 else 0
        out["effective_date"] = datetime.strptime(f"{m.group(1)} {m.group(2)} {year}", "%d %B %Y").date().isoformat()
    out["notes"]="Domestic resident callable table below ₹3 crore; senior rates exclude NRO/NRE."
    return out
