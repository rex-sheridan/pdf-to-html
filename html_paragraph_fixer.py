#!/usr/bin/env python3
"""
html_paragraph_fixer.py

Post-process OCR-generated HTML to combine paragraphs based on natural sentence boundaries.
Usage: python html_paragraph_fixer.py input.html output.html
"""

import sys
from bs4 import BeautifulSoup
import re

def is_attribution_line(text):
    """
    Check if the text appears to be an attribution line (author, source, etc.)
    """
    # Match patterns like "—AUTHOR NAME, WORK, NUMBER" or "-AUTHOR NAME"
    return bool(re.match(r'^[-—]\s*[A-Z\s,\.]+', text.strip()))

def should_combine_paragraphs(current_text, next_text):
    """
    Determine if two paragraph texts should be combined based on various heuristics.
    """
    if not current_text:
        return True  # Empty paragraphs should be combined with the next one
    
    if not next_text:
        return True  # Empty paragraphs should be combined with the previous one
    
    current_text = current_text.strip()
    next_text = next_text.strip()
    
    # Don't combine if next text is an attribution line
    if is_attribution_line(next_text):
        return False
    
    # Don't combine if current text ends with a clear sentence ending AND next starts with a capital
    if re.search(r'[.!?:]\s*$', current_text) and re.match(r'^[A-Z]', next_text):
        # Exception: if the next text starts with common continuation words
        continuation_words = r'^(said|continued|replied|added|explained|noted|suggested|mentioned|argued|concluded|wrote|stated|observed|remarked|responded)'
        if re.match(continuation_words, next_text.lower()):
            return True
        return False
    
    # Don't combine if either paragraph is very short (likely a heading or title)
    # BUT allow combining if one is empty or very short (likely a formatting artifact)
    if (len(current_text) >= 20 and len(next_text) >= 20) and (len(current_text.strip()) < 40 or len(next_text.strip()) < 40):
        return False
    
    # Combine if current text ends with a word that got cut off
    if re.search(r'[a-zA-Z]-\s*$', current_text):
        return True
    
    # Combine if current text ends with a word that suggests continuation
    continuation_indicators = r'(or|and|the|a|an|in|on|at|to|for|with|by|as|of|,)$'
    if re.search(continuation_indicators, current_text.lower()):
        return True
    
    # Combine if current text doesn't end with sentence-ending punctuation
    # or if next text doesn't start with a capital letter
    if not re.search(r'[.!?:]\s*$', current_text) or not re.match(r'^[A-Z]', next_text):
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
                current_text = current_p.get_text().rstrip()
                next_text = next_p.get_text().lstrip()
                
                # If both parts have content, add a space between them
                if current_text and next_text:
                    combined_text = current_text + ' ' + next_text
                else:
                    combined_text = current_text + next_text
                
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