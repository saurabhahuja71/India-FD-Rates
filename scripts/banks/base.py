import html, re
from html.parser import HTMLParser

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self._row=None; self._cell=None; self._text=[]
    def handle_starttag(self, tag, attrs):
        if tag == "tr": self._row=[]
        elif tag in ("td", "th") and self._row is not None: self._cell=[]
    def handle_data(self, data):
        if self._cell is not None: self._cell.append(data)
    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._row.append(re.sub(r"\s+", " ", " ".join(self._cell)).strip()); self._cell=None
        elif tag == "tr" and self._row:
            self.rows.append(self._row); self._row=None

def clean(raw):
    if isinstance(raw, bytes): raw = raw.decode("utf-8", "ignore")
    return html.unescape(html.unescape(raw))

def rows_from_html(raw, marker=None, stop=None):
    text = clean(raw)
    if marker:
        found = re.search(marker, text, re.I)
        if not found: raise ValueError(f"retail section marker not found: {marker}")
        text = text[found.start():]
    if stop:
        found = re.search(stop, text[500:], re.I)
        if found: text = text[:found.start() + 500]
    parser = TableParser(); parser.feed(text)
    rows=[]
    for cells in parser.rows:
        joined=" | ".join(cells)
        if re.search(r"\b(?:day|days|month|months|year|years|tenor|tenure)\b", joined, re.I):
            rates=re.findall(r"(\d+(?:\.\d+)?)\s*%", joined)
            if len(rates) >= 2 and not re.search(r"bulk|institutional|non.?callable|senior citizen only", joined, re.I):
                rows.append((cells[0], float(rates[-2]), float(rates[-1]), joined))
    if not rows: raise ValueError("no eligible retail rate rows found")
    return rows

def result_from_rows(rows, effective_date=None, source_type="official_bank_website"):
    regular=max(rows,key=lambda x:x[1]); senior=max(rows,key=lambda x:x[2])
    return {"regular_rate":regular[1],"regular_tenure":regular[0],"senior_rate":senior[2],"senior_tenure":senior[0],"effective_date":effective_date,"source_type":source_type,"evidence":{"matched_tenure":regular[0],"matched_regular_rate":f"{regular[1]:.2f}%","matched_senior_rate":f"{senior[2]:.2f}%"},"row_count":len(rows)}

def parse_html(raw, marker=None, stop=None, effective_date=None):
    return result_from_rows(rows_from_html(raw, marker, stop), effective_date)
