#!/usr/bin/env python3
"""
html_paragraph_fixer.py

Post-process OCR-generated HTML to combine paragraphs based on natural sentence boundaries.
Usage: python html_paragraph_fixer.py input.html output.html
"""

import sys
from bs4 import BeautifulSoup
import re

def is_valid_single_letter(text):
    """
    Check if a single letter is a valid standalone word.
    """
    valid_singles = {'A', 'I', 'O'}  # Common valid single-letter words in English
    return text.strip() in valid_singles

def should_join_letter_with_word(current_text, next_text):
    """
    Determine if a single letter should be joined with the next word.
    Example: "B y" should become "By", but "I am" should stay as is.
    Also handles cases where a letter is followed by a space in the same paragraph.
    """
    current_text = current_text.strip()
    next_text = next_text.strip()
    
    print(f"\nChecking letter join for: '{current_text}' + '{next_text}'")
    
    # Common word patterns to check against
    common_word_starts = [
        'By', 'Be', 'So', 'To', 'The', 'This', 'That', 'These', 'Those',
        'She', 'Some', 'Such', 'Since', 'Say', 'See', 'Said', 'Saw',
        'Stoicism', 'There', 'They', 'Then', 'Think', 'Thought',
        'When', 'Where', 'Which', 'While', 'Who', 'Whose', 'Whom',
        'What', 'Why', 'Will', 'Would', 'Were', 'With'
    ]
    
    # Check if current text is a sequence of single letters with spaces
    if re.match(r'^[A-Z](\s+[a-z])*$', current_text):
        # Join all letters together
        letters = ''.join(current_text.split())
        
        # Check if it forms a common word
        matches = [word for word in common_word_starts if letters.startswith(word)]
        if matches:
            print(f"  Joining: Split letters form word {matches[0]}")
            return True, letters
    
    # Check if current text starts with a single capital letter followed by space
    if re.match(r'^[A-Z]\s+\w', current_text):
        first_letter = current_text[0]
        rest_of_text = current_text[1:].lstrip()
        
        # Don't join if it's a valid single-letter word
        if is_valid_single_letter(first_letter):
            print("  Not joining: First letter is a valid single letter word")
            return False
            
        # Check if combining would form a common word
        combined = first_letter + rest_of_text
        
        matches = [word for word in common_word_starts if combined.startswith(word)]
        if matches:
            print(f"  Joining: Split word matches pattern {matches[0]}")
            # Return the combined text to be used
            return True, combined
        
        print("  Not joining: No matching word pattern for split word")
        return False
    
    # Original logic for separate paragraph cases
    if len(current_text) != 1 or not current_text.isupper():
        print("  Not joining: Current text is not a single capital letter")
        return False
    
    # Don't join if it's a valid single-letter word
    if is_valid_single_letter(current_text):
        print("  Not joining: Current text is a valid single letter word")
        return False
    
    # Check if next text starts with a lowercase letter
    if not next_text or not next_text[0].islower():
        print("  Not joining: Next text doesn't start with lowercase")
        return False
    
    # Check common word patterns when joined
    combined = current_text + next_text
    
    matches = [word for word in common_word_starts if combined.startswith(word)]
    if matches:
        print(f"  Joining: Matches pattern {matches[0]}")
        return True
    else:
        print("  Not joining: No matching word pattern")
        return False

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
    
    # Check for single letter that should be joined with next word
    if should_join_letter_with_word(current_text, next_text):
        return True
    
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
    Returns the modified HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Process each page section (marked by h2 tags) separately
    page_sections = soup.find_all('h2')
    
    for section in page_sections:
        # Get all paragraphs in this section
        paragraphs = []
        current = section.find_next_sibling()
        while current and current.name != 'h2':
            if current.name == 'p':
                paragraphs.append(current)
            current = current.find_next_sibling()
        
        i = 0
        while i < len(paragraphs) - 1:
            current_p = paragraphs[i]
            next_p = paragraphs[i + 1]
            
            current_text = current_p.get_text().strip()
            next_text = next_p.get_text().strip()
            
            print(f"\nChecking paragraphs:")
            print(f"Current: '{current_text}'")
            print(f"Next: '{next_text}'")
            
            # First check if we need to join a single letter with a word
            should_join, joined_text = False, None
            join_result = should_join_letter_with_word(current_text, next_text)
            
            if isinstance(join_result, tuple):
                should_join, joined_text = join_result
            else:
                should_join = join_result
            
            if should_join:
                print("Joining letter with word")
                if joined_text:
                    # Use the joined text if provided
                    current_p.string = joined_text
                else:
                    # Otherwise combine current and next
                    current_p.string = current_text + next_text
                next_p.decompose()
                paragraphs.pop(i + 1)
                continue
            
            # Then check if paragraphs should be combined
            if should_combine_paragraphs(current_text, next_text):
                print("Combining paragraphs")
                # Add a space between paragraphs when combining
                current_p.string = current_text + " " + next_text
                next_p.decompose()
                paragraphs.pop(i + 1)
            else:
                print("Not combining paragraphs")
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