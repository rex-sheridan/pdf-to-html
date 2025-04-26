#!/usr/bin/env python3
"""
html_paragraph_fixer.py

Post-process OCR-generated HTML to combine paragraphs based on natural sentence boundaries.
Usage: python html_paragraph_fixer.py input.html output.html
"""

import sys
from bs4 import BeautifulSoup
import re

def should_combine_paragraphs(current_text, next_text):
    """
    Determine if two paragraph texts should be combined based on various heuristics.
    """
    if not current_text or not next_text:
        return False
        
    # Don't combine if current text ends with a clear sentence ending
    if re.search(r'[.!?:]\s*$', current_text):
        return False
        
    # Don't combine if next text starts with a capital letter and previous ends with period
    if re.search(r'\.\s*$', current_text) and re.match(r'^[A-Z]', next_text):
        return False
        
    # Don't combine if either paragraph is very short (likely a heading or title)
    if len(current_text.strip()) < 20 or len(next_text.strip()) < 20:
        return False
        
    # Combine if current text ends with a word that got cut off
    if re.search(r'[a-zA-Z]-\s*$', current_text):
        return True
        
    # Combine if current text doesn't end with punctuation and next doesn't start with capital
    if not re.search(r'[.!?:]\s*$', current_text) and not re.match(r'^[A-Z]', next_text):
        return True
        
    return False

def fix_paragraphs(html_content):
    """
    Process HTML content to combine paragraphs where appropriate.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Process each page section
    for page_section in soup.find_all('h2'):
        paragraphs = []
        current = page_section.find_next('p')
        
        while current and (not current.find_previous('h2') or current.find_previous('h2') == page_section):
            if current.name == 'p':
                paragraphs.append(current)
            current = current.find_next()
        
        # Combine paragraphs where appropriate
        i = 0
        while i < len(paragraphs) - 1:
            current_p = paragraphs[i]
            next_p = paragraphs[i + 1]
            
            if should_combine_paragraphs(current_p.get_text(), next_p.get_text()):
                # Add a space between combined text if needed
                combined_text = current_p.get_text().rstrip() + ' ' + next_p.get_text().lstrip()
                current_p.string = combined_text
                next_p.decompose()
                paragraphs.pop(i + 1)
            else:
                i += 1
    
    return str(soup)

def main():
    if len(sys.argv) < 3:
        print("Usage: python html_paragraph_fixer.py input.html output.html")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Read input HTML
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Process and fix paragraphs
    fixed_html = fix_paragraphs(html_content)
    
    # Write output HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(fixed_html)

if __name__ == "__main__":
    main() 