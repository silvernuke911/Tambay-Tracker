import pdfplumber
import re
from pathlib import Path

def read_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

form5_dir = Path(r"C:\Users\verci\Documents\code\Tambay-Tracker\AutoMobChart1.0\tests\sample_form5")
pdf_files = list(form5_dir.glob("*.pdf"))  # Only .pdf files
