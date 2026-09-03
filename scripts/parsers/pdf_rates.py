"""Text extraction helpers for official, text-based bank rate-card PDFs.

Image-only PDFs are deliberately rejected: OCR would make the evidence less
deterministic and is not needed for the supported official rate cards.
"""
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple


def extract_text(raw: bytes) -> Tuple[str, int]:
    """Return PDF text and page count, without OCR."""
    try:
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(raw))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        if not text.strip():
            raise ValueError("PDF is image-only or contains no extractable text")
        return text, len(reader.pages)
    except ImportError:
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "rates.pdf"
            txt = Path(tmp) / "rates.txt"
            pdf.write_bytes(raw)
            try:
                subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True,
                               capture_output=True, timeout=20)
            except (FileNotFoundError, subprocess.CalledProcessError) as exc:
                raise ValueError("install pypdf or pdftotext to read official PDFs") from exc
            text = txt.read_text(errors="ignore")
            if not text.strip():
                raise ValueError("PDF is image-only or contains no extractable text")
            return text, text.count("\f") + 1


def effective_date(text: str) -> Optional[str]:
    match = re.search(r"(?:effective|applicable|w.e.f\.?|from)\D{0,30}"
                      r"(\d{1,2})[\s/-]+([A-Za-z]{3,9}|\d{1,2})[\s/-]+(20\d{2})", text, re.I)
    if not match:
        return None
    from datetime import datetime
    value = " ".join(match.groups())
    for fmt in ("%d %B %Y", "%d %b %Y", "%d %m %Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return None
