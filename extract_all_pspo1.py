#!/usr/bin/env python3
"""
Extract all PSPO1 questions from PDF and format them for database import.
"""

import pdfplumber
import json
import re
import sys

def extract_all_pspo1_questions():
    questions = []
    
    try:
        with pdfplumber.open('PSPO1_v1.2.1.pdf') as pdf:
            print(f"Processing PDF with {len(pdf.pages)} pages...")
            
            all_text = ""
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
                    
                if page_num % 10 == 0:
                    print(f"Processed page {page_num + 1}/{len(pdf.pages)}")
            
            print(f"Extracted {len(all_text)} characters of text")
            
            # Split by questions - look for numbered patterns
            lines = all_text.split('\n')
            
            current_question = None
            current_choices = []
            current_number = 0
            in_answers = False
            
            for line_idx, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                    
                # Skip headers and page numbers
                if 'PSPO1_v1.2.1.md' in line or line.startswith('⬆') or line == 'Table of Contents':
                    continue
                
                # Look for numbered questions - more flexible pattern
                question_match = re.match(r'^(\d+)\s*(.*)', line)
                if question_match:
                    # Save previous question if it exists and has choices
                    if current_question and len(current_choices) >= 2:
                        questions.append({
                            'number': current_number,
                            'text': current_question.strip(),
                            'choices': current_choices[:4],  # Max 4 choices
                            'explanation': 'PSPO1'
                        })
                    
                    # Start new question
                    current_number = int(question_match.group(1))
                    current_question = question_match.group(2).strip()
                    current_choices = []
                    in_answers = False
                    
                # Look for True/False questions
                elif re.match(r'^True or False:', line) and not current_question:
                    current_number += 1
                    current_question = line
                    current_choices = ['True', 'False']
                    in_answers = False
                
                # Look for choice indicators - letters or bullet points
                elif re.match(r'^[A-D][\.\)]\s*', line):
                    choice_text = re.sub(r'^[A-D][\.\)]\s*', '', line).strip()
                    if choice_text:
                        current_choices.append(choice_text)
                        in_answers = True
                
                # Look for other choice patterns
                elif re.match(r'^[a-d][\.\)]\s*', line):
                    choice_text = re.sub(r'^[a-d][\.\)]\s*', '', line).strip()
                    if choice_text:
                        current_choices.append(choice_text)
                        in_answers = True
                
                # Look for numbered choices
                elif re.match(r'^\d+[\.\)]\s+[A-Z]', line) and in_answers:
                    choice_text = re.sub(r'^\d+[\.\)]\s*', '', line).strip()
                    if choice_text and len(current_choices) < 4:
                        current_choices.append(choice_text)
                
                # Continue question text if we haven't found choices yet
                elif current_question and not in_answers and not re.match(r'^[A-Za-z][\.\)]', line):
                    # Add to current question if it's a continuation
                    if not re.match(r'^\d+', line):
                        current_question += ' ' + line
                
                # Look for answer choices in different formats
                elif current_question and not in_answers:
                    # Check if this could be start of choices
                    if any(keyword in line.lower() for keyword in ['choose', 'select', 'answer']):
                        # This might be instruction text, continue question
                        current_question += ' ' + line
                    elif len(line) > 10 and not re.match(r'^\d+', line):
                        # Could be a choice without letter prefix
                        if '?' not in line and len(current_choices) < 4:
                            current_choices.append(line)
                            in_answers = True
            
            # Don't forget the last question
            if current_question and len(current_choices) >= 2:
                questions.append({
                    'number': current_number,
                    'text': current_question.strip(),
                    'choices': current_choices[:4],
                    'explanation': 'PSPO1'
                })
            
            print(f"Successfully extracted {len(questions)} questions")
            
            # Filter out questions that are too short or malformed
            valid_questions = []
            for q in questions:
                if (len(q['text']) > 20 and 
                    len(q['choices']) >= 2 and
                    all(len(choice) > 5 for choice in q['choices'])):
                    valid_questions.append(q)
            
            print(f"Filtered to {len(valid_questions)} valid questions")
            return valid_questions
            
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []

def main():
    questions = extract_all_pspo1_questions()
    
    if not questions:
        print("No questions extracted!")
        return
    
    # Save all questions to JSON file
    with open('all_pspo1_questions_complete.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved {len(questions)} questions to 'all_pspo1_questions_complete.json'")
    
    # Show sample questions
    print("\n=== Sample Questions ===")
    for i, q in enumerate(questions[:5]):
        print(f"\nQuestion {i+1} (#{q['number']}):")
        print(f"Text: {q['text'][:150]}...")
        print(f"Choices ({len(q['choices'])}):")
        for j, choice in enumerate(q['choices']):
            print(f"  {chr(65+j)}) {choice[:80]}...")
    
    print(f"\n=== Statistics ===")
    print(f"Total questions: {len(questions)}")
    print(f"Questions with 2 choices: {sum(1 for q in questions if len(q['choices']) == 2)}")
    print(f"Questions with 3 choices: {sum(1 for q in questions if len(q['choices']) == 3)}")
    print(f"Questions with 4 choices: {sum(1 for q in questions if len(q['choices']) == 4)}")

if __name__ == "__main__":
    main()