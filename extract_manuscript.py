#!/usr/bin/env python3
"""
Faroese Manuscript Text Extractor
Extracts clean text content from HTML manuscript file while preserving structure.
"""

import re
from bs4 import BeautifulSoup
import os

def clean_text(text):
    """Clean up whitespace and formatting in text."""
    if not text:
        return ""
    # Remove extra whitespace but preserve intentional line breaks
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def extract_manuscript_text(input_file, output_file):
    """Extract text content from HTML manuscript file."""
    
    print(f"Reading from: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main content sections
    sections = soup.find_all('section', class_=['ms', 'scene-s', 'song-s', 'part-s'])
    
    extracted_text = []
    extracted_text.append("KLOKKARIN Í NOTRE DAME")
    extracted_text.append("Leikrit")
    extracted_text.append("=" * 50)
    extracted_text.append("")
    
    for section in sections:
        # Extract section title
        title_elem = section.find(['h2', 'h3', 'h4'], class_='sh')
        if title_elem:
            title = clean_text(title_elem.get_text())
            if title:
                extracted_text.append("")
                extracted_text.append(title.upper())
                extracted_text.append("-" * len(title))
                extracted_text.append("")
        
        # Extract content from the section
        content_div = section.find('div', class_='sb')
        if content_div:
            
            # Process paragraphs
            paragraphs = content_div.find_all('p')
            
            for p in paragraphs:
                paragraph_text = ""
                
                # Check if this paragraph contains a character name
                char_span = p.find('span', class_='ch')
                if char_span:
                    char_name = clean_text(char_span.get_text())
                    
                    # Handle song titles (in italics)
                    if char_name.startswith('#') or char_name.startswith('*'):
                        paragraph_text = f"♪ {char_name} ♪"
                    else:
                        # Regular character name
                        paragraph_text = f"{char_name}:"
                    
                    # Remove the character span and get remaining text
                    char_span.decompose()
                    remaining_text = clean_text(p.get_text())
                    if remaining_text:
                        paragraph_text += f" {remaining_text}"
                else:
                    # Regular paragraph text
                    text_content = clean_text(p.get_text())
                    
                    # Check if it's a stage direction (starts with asterisk or in parentheses)
                    if text_content.startswith('*') and text_content.endswith('*'):
                        paragraph_text = f"({text_content[1:-1]})"
                    elif text_content.startswith('(') and text_content.endswith(')'):
                        paragraph_text = text_content
                    else:
                        paragraph_text = text_content
                
                if paragraph_text.strip():
                    extracted_text.append(paragraph_text)
            
            # Add spacing after each section
            extracted_text.append("")
    
    # Write to output file
    print(f"Writing to: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in extracted_text:
            f.write(line + '\n')
    
    print(f"Extraction complete! Text saved to {output_file}")
    print(f"Total lines extracted: {len(extracted_text)}")

def main():
    """Main function to run the extraction."""
    
    input_file = "index.html"
    output_file = "klokkarin_manuscript_clean.txt"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found in current directory")
        print("Please make sure the HTML file is in the same directory as this script.")
        return
    
    try:
        extract_manuscript_text(input_file, output_file)
        print("\n" + "="*60)
        print("SUCCESS: Clean manuscript text has been extracted!")
        print(f"You can now edit '{output_file}' in any word processor.")
        print("="*60)
        
    except Exception as e:
        print(f"Error during extraction: {e}")

if __name__ == "__main__":
    main()