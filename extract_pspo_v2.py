import pdfplumber
import re
import json

def extract_pspo_questions_v2(pdf_path):
    """Extract PSPO1 questions from PDF - improved version"""
    questions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    
    print(f"PDF gelezen, totaal {len(full_text)} karakters")
    
    # Split tekst in lijnen
    lines = full_text.split('\n')
    
    current_question = None
    current_answers = []
    answer_options = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip lege lijnen en headers
        if not line or 'PSPO1_v1.2.1.md' in line or line == 'No. Questions':
            i += 1
            continue
        
        # Check if line starts with question number
        question_match = re.match(r'^(\d+)(?:\s|$)', line)
        
        if question_match:
            # Save previous question if exists
            if current_question and len(answer_options) >= 2:
                questions.append({
                    "number": current_question["number"],
                    "question": current_question["text"],
                    "answers": answer_options[:4],  # Max 4 answers
                    "correct": [0]  # Default eerste antwoord, wordt later aangepast
                })
            
            # Start nieuwe vraag
            question_num = int(question_match.group(1))
            question_text = line[len(question_match.group(0)):].strip()
            
            # Verzamel volledige vraag tekst (kan over meerdere lijnen staan)
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^[A-D]\)', lines[i].strip()) and not re.match(r'^(\d+)(?:\s|$)', lines[i].strip()):
                question_text += " " + lines[i].strip()
                i += 1
            
            current_question = {
                "number": question_num,
                "text": question_text.strip()
            }
            answer_options = []
            continue
        
        # Check for answer options (A), B), C), D))
        answer_match = re.match(r'^([A-D])\)\s*(.+)', line)
        if answer_match:
            letter = answer_match.group(1)
            answer_text = answer_match.group(2).strip()
            
            # Verzamel volledig antwoord (kan over meerdere lijnen staan)
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^[A-D]\)', lines[i].strip()) and not re.match(r'^(\d+)(?:\s|$)', lines[i].strip()):
                answer_text += " " + lines[i].strip()
                i += 1
            
            answer_options.append(answer_text.strip())
            continue
        
        i += 1
    
    # Don't forget last question
    if current_question and len(answer_options) >= 2:
        questions.append({
            "number": current_question["number"],
            "question": current_question["text"],
            "answers": answer_options[:4],
            "correct": [0]  # Default
        })
    
    print(f"Gevonden {len(questions)} vragen")
    
    # Try to find correct answers by looking for answer key section
    answer_key_found = False
    correct_answers = {}
    
    # Look for patterns like "1. A" or "Question 1: A"
    answer_key_pattern = r'(\d+)[\.\s:]*([A-D])'
    answer_matches = re.findall(answer_key_pattern, full_text)
    
    if answer_matches:
        print(f"Gevonden {len(answer_matches)} correcte antwoorden")
        for q_num, correct_letter in answer_matches:
            correct_answers[int(q_num)] = ord(correct_letter) - ord('A')
        answer_key_found = True
    
    # Update correct answers
    for q in questions:
        if q["number"] in correct_answers:
            q["correct"] = [correct_answers[q["number"]]]
    
    return questions, answer_key_found

if __name__ == "__main__":
    pdf_path = "/root/quiz-app/PSPO1_v1.2.1.pdf"
    
    print("🔍 Extracting PSPO1 vragen uit PDF (versie 2)...")
    questions, answer_key_found = extract_pspo_questions_v2(pdf_path)
    
    print(f"\n=== RESULTAAT ===")
    print(f"✅ Gevonden: {len(questions)} vragen")
    print(f"📝 Antwoordsleutel gevonden: {'Ja' if answer_key_found else 'Nee'}")
    
    # Save to JSON
    with open("/root/quiz-app/pspo1_questions_v2.json", 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    # Show first few questions
    print(f"\n=== VOORBEELDEN ===")
    for i, q in enumerate(questions[:3]):
        print(f"\n--- Vraag {q['number']} ---")
        print(f"Tekst: {q['question'][:100]}...")
        print(f"Antwoorden:")
        for j, ans in enumerate(q['answers']):
            marker = "✓" if j in q['correct'] else " "
            print(f"  {chr(65+j)}. {ans[:80]}{'...' if len(ans) > 80 else ''} {marker}")
    
    print(f"\n📁 Vragen opgeslagen in pspo1_questions_v2.json")
    print(f"🎯 Volgende stap: toevoegen aan database als 'PSPO1' categorie")