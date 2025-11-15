#!/usr/bin/env python3
"""
Improved PSPO1 question extractor based on the actual PDF format.
"""

import pdfplumber
import json
import re

def extract_pspo1_questions_v2():
    questions = []
    
    with pdfplumber.open('PSPO1_v1.2.1.pdf') as pdf:
        print(f"Processing {len(pdf.pages)} pages...")
        
        all_lines = []
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and 'PSPO1_v1.2.1.md' not in line:
                        all_lines.append(line)
                        
            if page_num % 10 == 0:
                print(f"Processed page {page_num + 1}")
        
        print(f"Total lines: {len(all_lines)}")
        
        i = 0
        question_count = 0
        
        while i < len(all_lines):
            line = all_lines[i]
            
            # Pattern 1: True/False questions
            if 'True or False:' in line:
                question_text = line
                question_count += 1
                questions.append({
                    'number': question_count,
                    'text': question_text,
                    'choices': ['True', 'False'],
                    'explanation': 'PSPO1'
                })
                print(f"Found T/F question {question_count}: {question_text[:50]}...")
                
            # Pattern 2: Multiple choice questions ending with "(choose the best"
            elif 'choose the best' in line.lower() or 'choose all that apply' in line.lower():
                # Look backwards to find the question start
                question_lines = []
                j = i
                while j >= 0:
                    current_line = all_lines[j]
                    # Stop if we hit a number that could be a question number
                    if re.match(r'^\d+$', current_line) and j < i:
                        break
                    if re.match(r'^\d+\s', current_line):
                        # This line starts with a number, likely question number + text
                        question_text = re.sub(r'^\d+\s*', '', current_line)
                        question_lines.insert(0, question_text)
                        break
                    elif current_line and not current_line.isdigit():
                        question_lines.insert(0, current_line)
                    j -= 1
                
                if question_lines:
                    full_question = ' '.join(question_lines)
                    # Now look forward for answer choices
                    choices = []
                    k = i + 1
                    while k < len(all_lines) and len(choices) < 6:
                        choice_line = all_lines[k]
                        # Stop at next question or empty line
                        if (re.match(r'^\d+$', choice_line) or 
                            'True or False:' in choice_line or
                            'choose the best' in choice_line.lower() or
                            not choice_line.strip()):
                            break
                        # Remove letter prefixes A) B) etc
                        clean_choice = re.sub(r'^[A-Za-z][\)\.]?\s*', '', choice_line)
                        if clean_choice and len(clean_choice) > 5:
                            choices.append(clean_choice)
                        k += 1
                    
                    if len(choices) >= 2:
                        question_count += 1
                        questions.append({
                            'number': question_count,
                            'text': full_question,
                            'choices': choices[:4],  # Limit to 4 choices
                            'explanation': 'PSPO1'
                        })
                        print(f"Found MC question {question_count}: {full_question[:50]}...")
                        i = k - 1  # Skip processed lines
            
            # Pattern 3: Questions starting with a number
            elif re.match(r'^\d+\s+[A-Z]', line) and '?' in line:
                question_text = re.sub(r'^\d+\s+', '', line)
                # Look for choices on following lines
                choices = []
                j = i + 1
                while j < len(all_lines) and len(choices) < 4:
                    choice_line = all_lines[j]
                    if (re.match(r'^\d+\s', choice_line) or 
                        'True or False:' in choice_line or
                        not choice_line.strip()):
                        break
                    clean_choice = re.sub(r'^[A-Za-z][\)\.]?\s*', '', choice_line)
                    if clean_choice and len(clean_choice) > 5:
                        choices.append(clean_choice)
                    j += 1
                
                if len(choices) >= 2:
                    question_count += 1
                    questions.append({
                        'number': question_count,
                        'text': question_text,
                        'choices': choices,
                        'explanation': 'PSPO1'
                    })
                    print(f"Found numbered question {question_count}: {question_text[:50]}...")
                    i = j - 1  # Skip processed lines
            
            i += 1
        
        print(f"\\nExtracted {len(questions)} questions total")
        return questions

def main():
    questions = extract_pspo1_questions_v2()
    
    # Save to JSON
    with open('pspo1_complete_v2.json', 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"\\nSaved {len(questions)} questions to pspo1_complete_v2.json")
    
    # Show samples
    print("\\n=== Sample Questions ===")
    for i, q in enumerate(questions[:3]):
        print(f"\\nQuestion {i+1}:")
        print(f"Text: {q['text'][:100]}...")
        print(f"Choices: {q['choices']}")
    
    # Statistics
    print(f"\\n=== Statistics ===")
    true_false = sum(1 for q in questions if len(q['choices']) == 2 and 'True' in q['choices'])
    multiple_choice = len(questions) - true_false
    print(f"True/False questions: {true_false}")
    print(f"Multiple choice questions: {multiple_choice}")
    print(f"Total questions: {len(questions)}")

if __name__ == '__main__':
    main()