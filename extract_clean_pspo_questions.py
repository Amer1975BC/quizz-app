#!/usr/bin/env python3
"""
Clean PSPO1 PDF Question Extractor
Extracts and properly formats questions from the PSPO1 certification PDF
"""

import re
import json
import pdfplumber
from typing import List, Dict, Any

def extract_questions_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract questions using a more focused approach"""
    questions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        
        # Extract text from all pages
        for page_num, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:
                # Clean page text
                page_text = clean_page_text(page_text)
                all_text += page_text + "\n\n"
                print(f"Processing page {page_num}/{len(pdf.pages)}")
    
    # Now parse the questions
    questions = parse_questions_from_text(all_text)
    return questions

def clean_page_text(text: str) -> str:
    """Clean individual page text"""
    if not text:
        return ""
    
    # Remove headers/footers
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip page numbers, headers, footers
        if re.match(r'^(Page \d+|www\.|This document|Professional Scrum)', line, re.IGNORECASE):
            continue
        if re.match(r'^\d+\s*/\s*\d+\s*$', line):  # Skip "1 / 64" style lines
            continue
        if len(line) > 0:
            cleaned_lines.append(line)
    
    return ' '.join(cleaned_lines)

def parse_questions_from_text(text: str) -> List[Dict[str, Any]]:
    """Parse questions from cleaned text"""
    questions = []
    
    # Try different question patterns
    patterns = [
        # Pattern 1: Question number followed by text
        r'(\d+)\.\s+(.+?)(?=\d+\.|$)',
        # Pattern 2: Look for True/False questions
        r'(True or False[:\s]*(.+?)(?=True or False|$))',
        # Pattern 3: Multiple choice indicators
        r'(Which of the following.+?)(?=Which of the following|$)',
        # Pattern 4: Choose the best answer
        r'(.+?choose the best answer[^\n]*)\s*([A-E]\..*?)(?=.+?choose the best answer|$)',
    ]
    
    # Split text into potential question blocks
    question_blocks = []
    
    # Method 1: Split by question numbers
    number_pattern = r'(\d+)\.\s+'
    parts = re.split(number_pattern, text)
    
    if len(parts) > 3:  # We found numbered questions
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                question_num = parts[i]
                question_content = parts[i + 1]
                question_blocks.append((question_num, question_content))
    
    # Process each question block
    for question_num, content in question_blocks:
        question_data = process_question_block(question_num, content)
        if question_data:
            questions.append(question_data)
    
    return questions

def process_question_block(question_num: str, content: str) -> Dict[str, Any]:
    """Process individual question block"""
    content = content.strip()
    
    if len(content) < 20:  # Too short to be a real question
        return None
    
    # Look for answer choices
    answers = []
    question_text = content
    
    # Pattern 1: A. B. C. D. style
    choice_pattern = r'([A-E])\.\s*([^A-E]+?)(?=[A-E]\.|$)'
    matches = re.findall(choice_pattern, content, re.DOTALL)
    
    if matches:
        answers = [match[1].strip() for match in matches]
        # Extract question text (everything before first choice)
        first_choice_pos = content.find(matches[0][0] + '.')
        if first_choice_pos > 0:
            question_text = content[:first_choice_pos].strip()
    
    # Pattern 2: True/False
    elif 'true' in content.lower() and 'false' in content.lower():
        answers = ['True', 'False']
        question_text = content
    
    # Pattern 3: Bullet points or numbered lists
    elif re.search(r'^\s*[-•▪]\s+', content, re.MULTILINE):
        bullet_matches = re.findall(r'^\s*[-•▪]\s+(.+)', content, re.MULTILINE)
        if len(bullet_matches) >= 2:
            answers = [match.strip() for match in bullet_matches]
            # Extract question before bullets
            first_bullet_pos = content.find('•')
            if first_bullet_pos < 0:
                first_bullet_pos = content.find('-')
            if first_bullet_pos > 0:
                question_text = content[:first_bullet_pos].strip()
    
    # Clean up question text
    question_text = clean_question_text(question_text)
    answers = [clean_answer_text(ans) for ans in answers if clean_answer_text(ans)]
    
    # Validate question
    if len(question_text) < 10 or len(answers) < 2:
        return None
    
    return {
        "text": question_text,
        "choices": answers[:6],  # Max 6 choices
        "explanation": "PSPO1",
        "difficulty": "medium"
    }

def clean_question_text(text: str) -> str:
    """Clean question text"""
    if not text:
        return ""
    
    # Remove common artifacts
    text = re.sub(r'^\d+\.\s*', '', text)  # Remove question number
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = re.sub(r'choose the best answer[.:]?\s*$', '', text, re.IGNORECASE)
    
    return text.strip()

def clean_answer_text(text: str) -> str:
    """Clean answer text"""
    if not text:
        return ""
    
    text = re.sub(r'^[A-E]\.\s*', '', text)  # Remove choice letter
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    
    return text.strip()

def main():
    """Main function"""
    pdf_path = "PSPO1_v1.2.1.pdf"
    
    print(f"🔍 Extracting questions from {pdf_path}...")
    
    try:
        questions = extract_questions_from_pdf(pdf_path)
        
        print(f"✅ Extracted {len(questions)} questions")
        
        if questions:
            # Save to JSON
            output_file = "pspo1_clean_questions.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(questions, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved to {output_file}")
            
            # Show samples
            print("\n📋 Sample questions:")
            for i, q in enumerate(questions[:3]):
                print(f"\n{i+1}. {q['text'][:100]}...")
                for j, choice in enumerate(q['choices']):
                    print(f"   {chr(65+j)}. {choice[:50]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()