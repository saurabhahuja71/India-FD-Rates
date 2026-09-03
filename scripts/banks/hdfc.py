import re
from .base import clean, result_from_rows
def parse(raw):
    text=clean(raw); headings=list(re.finditer(r"Domestic\s*/\s*NRO\s*/\s*NRE\s+FIXED\s+DEPOSIT\s+RATE",text,re.I))
    if not headings: raise ValueError("HDFC domestic table heading not found")
    start=next((m for m in headings if re.search(r"<\s*3\s*Crore",text[m.start():m.start()+3000],re.I)),headings[0]); block=text[start.start():]
    nxt=re.search(r"Domestic\s*/\s*NRO\s*/\s*NRE\s+FIXED\s+DEPOSIT\s+RATE",block[1000:],re.I)
    if nxt: block=block[:nxt.start()+1000]
    date_match=re.search(r"Applicable\s+from\s+[^0-9]{0,30}?([0-9]{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+),\s+([0-9]{4})",block,re.I)
    effective=None
    if date_match:
        from datetime import datetime
        effective=datetime.strptime(" ".join(date_match.groups()),"%d %B %Y").date().isoformat()
    rows=[]
    for m in re.finditer(r"<tr[^>]*>\s*<td[^>]*>\s*(.*?)\s*</td>\s*<td[^>]*>\s*(\d+(?:\.\d+)?)%\s*</td>\s*<td[^>]*>\s*(\d+(?:\.\d+)?)%\s*</td>",block,re.I|re.S):
        tenure=re.sub(r"\s+"," ",re.sub(r"</?[A-Za-z][^>]*>","",m.group(1))).strip(); rows.append((tenure,float(m.group(2)),float(m.group(3)),""))
    return result_from_rows(rows,effective)
