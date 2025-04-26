#!/usr/bin/env python3
"""
ocr_to_html.py

Convert a scanned PDF to HTML by performing OCR on each page.
Usage: python ocr_to_html.py input.pdf output.html
"""

import os
import sys
from pdf2image import convert_from_path
import pytesseract
import html

def pdf_to_html_ocr(pdf_path, html_path, dpi=300, poppler_path=None):
    # Convert PDF pages to PIL images
    pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write("<!DOCTYPE html>\n<html lang='en'>\n")
        f.write("<head><meta charset='utf-8'><title>OCR: " + html.escape(os.path.basename(pdf_path)) + "</title></head>\n<body>\n")
        
        for i, page in enumerate(pages, start=1):
            text = pytesseract.image_to_string(page)
            f.write(f"<h2>Page {i}</h2>\n")
            for line in text.splitlines():
                f.write(f"<p>{html.escape(line)}</p>\n")
        
        f.write("</body>\n</html>")

def main():
    if len(sys.argv) < 3:
        print("Usage: python ocr_to_html.py input.pdf output.html")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    html_path = sys.argv[2]
    # Optional: adjust poppler_path if convert_from_path needs it on your system
    pdf_to_html_ocr(pdf_path, html_path)

if __name__ == "__main__":
    main()
