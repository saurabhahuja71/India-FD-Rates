import re
from .base import result_from_rows
from parsers.pdf_rates import extract_text, effective_date

def parse(raw):
    if not raw.startswith(b"%PDF"):
        from .base import parse_html
        return parse_html(raw)
    text, _ = extract_text(raw)
    start = re.search(r"Fixed Deposit Interest Rates.*?(?:less than|<)\s*INR?\s*3\s*Cr", text, re.I | re.S)
    if not start: raise ValueError("YES Bank domestic retail PDF section not found")
    rows=[]
    for line in text[start.end():].splitlines():
        m=re.match(r"\s*(.+?\S)\s+(\d+\.\d+)%\s+\d+\.\d+%\s+(\d+\.\d+)%",line)
        if m and re.search(r"day|month|year",m.group(1),re.I):
            rows.append((m.group(1).strip(),float(m.group(2)),float(m.group(3)),line.strip()))
    if not rows: raise ValueError("YES Bank domestic retail PDF rows not found")
    out=result_from_rows(rows, effective_date(text)); out["notes"]="Callable domestic retail FD; PDF includes NRO but senior rate is domestic-only."
    return out
