import re
from datetime import datetime
from .base import TableParser, clean, result_from_rows

def parse(raw):
    text=clean(raw); p=TableParser(); p.feed(text)
    # First table is the revised retail schedule. Later tables are historical,
    # non-callable, or bulk; selecting by headers prevents cross-table mixing.
    header=next((r for r in p.rows if r and r[0].strip().lower()=="period of deposits" and any("revised rates for deposits below" in c.lower() for c in r)),None)
    if not header: raise ValueError("IOB revised retail deposit table not found")
    revised=next(i for i,c in enumerate(header) if "revised rates for deposits below" in c.lower())
    if "non-callable" in header[revised].lower(): raise ValueError("IOB selected non-callable column")
    rows=[]
    for cells in p.rows[p.rows.index(header)+1:]:
        if not cells or re.match(r"period of deposit", cells[0].strip(), re.I) or re.search(r"bulk deposit", " ".join(cells), re.I): break
        if len(cells)>revised and re.search(r"day|year|month",cells[0],re.I):
            value=re.search(r"(\d+(?:\.\d+)?)",cells[revised])
            if value: rows.append((cells[0],float(value.group(1)),float(value.group(1))+0.50," | ".join(cells)))
    if not rows: raise ValueError("IOB revised callable retail rows not found")
    out=result_from_rows(rows)
    out.update({"callable":True,"customer_type":"RESIDENT_DOMESTIC_RETAIL_INDIVIDUAL","source_table":"Revised retail deposits below Rs. 3 Crore; callable counterpart to separately listed non-callable deposits","regular_source_column":header[revised],"senior_source_column":"Senior Citizen additional interest: +0.50% over applicable retail rate","notes":"IOB page separately lists non-callable rates and states an additional 0.50% for senior citizens; only the revised retail column was selected."})
    m=re.search(r"W\.E\.F\.?\s*(\d{1,2})[./-](\d{1,2})[./-](20\d{2})",header[revised],re.I)
    if m: out["effective_date"] = datetime.strptime("-".join(m.groups()),"%d-%m-%Y").date().isoformat()
    return out
