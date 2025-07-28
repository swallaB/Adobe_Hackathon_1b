import os
import fitz  # PyMuPDF
from typing import List, Dict

def load_pdf(file_path: str) -> str:
    """Extract full text from a single PDF file using PyMuPDF."""
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def load_all_pdfs(folder_path: str) -> List[Dict]:
    """
    Load all PDFs and return a list of dictionaries with doc title, text, and page numbers.
    """
    all_docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            with fitz.open(file_path) as doc:
                for i, page in enumerate(doc, start=1):
                    page_text = page.get_text().strip()
                    if page_text:  # Avoid empty pages
                        all_docs.append({
                            "title": filename,
                            "text": page_text,
                            "page_number": i
                        })
    return all_docs
