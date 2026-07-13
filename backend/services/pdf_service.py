import pdfplumber
from PyPDF2 import PdfReader
from pathlib import Path
from typing import List, Dict, Any

class PDFService:
    def extract_text(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract text page by page from the PDF.
        Returns a dict with complete text, list of pages, and page count.
        """
        pages_content = []
        full_text = ""
        
        # Try pdfplumber first
        try:
            with pdfplumber.open(file_path) as pdf:
                for idx, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    pages_content.append({
                        "page_num": idx + 1,
                        "text": text
                    })
                    full_text += f"\n--- PAGE {idx + 1} ---\n" + text
        except Exception as e:
            # Fallback to PyPDF2
            print(f"pdfplumber failed: {e}. Falling back to PyPDF2...")
            pages_content = []
            full_text = ""
            try:
                reader = PdfReader(file_path)
                for idx, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    pages_content.append({
                        "page_num": idx + 1,
                        "text": text
                    })
                    full_text += f"\n--- PAGE {idx + 1} ---\n" + text
            except Exception as e2:
                print(f"PyPDF2 failed as well: {e2}")
                raise ValueError(f"Could not parse PDF file: {e2}")
                
        return {
            "full_text": full_text,
            "pages": pages_content,
            "page_count": len(pages_content)
        }

pdf_service = PDFService()
