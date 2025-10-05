# extractor.py
from PyPDF2 import PdfReader
import docx
import os

def read_txt(path, max_chars=1000):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read(max_chars)

def read_pdf(path, max_chars=1000):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text
            if len(text) >= max_chars:
                break
        return text[:max_chars]
    except Exception as e:
        print("[extractor] PDF read error:", e)
        return ""

def read_docx(path, max_chars=1000):
    try:
        doc = docx.Document(path)
        text = "\n".join(p.text for p in doc.paragraphs)
        return text[:max_chars]
    except Exception as e:
        print("[extractor] DOCX read error:", e)
        return ""

def extract_snippet(path, max_chars=1000):
    path_lower = path.lower()
    if path_lower.endswith(".txt"):
        return read_txt(path, max_chars)
    if path_lower.endswith(".pdf"):
        return read_pdf(path, max_chars)
    if path_lower.endswith(".docx"):
        return read_docx(path, max_chars)
    # unknown file type -> return empty so main will skip AI tagging
    return ""
