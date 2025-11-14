import pdfplumber
import re
import json

def extract_pspo_questions(pdf_path):
    """Extract PSPO1 questions and answers from PDF"""
    questions = []
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        # Read all pages
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    
    print(f"PDF gelezen, totaal {len(full_text)} karakters")
    
    # Zoek naar verschillende vraag patronen
    patterns = [
        r'(\d+)\.\s*([^?\n]+\?)',  # Standaard: "1. Question text?"
        r'Q(\d+)[\.\s]*([^?\n]+\?)',  # Q1. Question text?
        r'Question\s+(\d+)[\.\s]*([^?\n]+\?)'  # Question 1. text?
    ]
    
    all_matches = []
    for pattern in patterns:
        matches = list(re.finditer(pattern, full_text, re.MULTILINE | re.DOTALL))
        all_matches.extend([(m.group(1), m.group(2).strip(), m.start(), m.end()) for m in matches])
    
    # Sorteer op positie in document
    all_matches.sort(key=lambda x: x[2])
    
    print(f"Gevonden {len(all_matches)} mogelijke vragen")
    
    for i, (question_num, question_text, start_pos, end_pos) in enumerate(all_matches):
        # Zoek naar antwoordsectie na de vraag
        if i + 1 < len(all_matches):
            next_start = all_matches[i + 1][2]
        else:
            next_start = len(full_text)
        
        # Extract text tussen deze vraag en de volgende
        answer_section = full_text[end_pos:next_start]
        
        # Zoek naar antwoordmogelijkheden (A, B, C, D of a, b, c, d)
        answer_patterns = [
            r'([A-D])\.\s*([^\n\r]+)',  # A. Answer text
            r'([A-D])\)\s*([^\n\r]+)',  # A) Answer text
            r'([a-d])\.\s*([^\n\r]+)',  # a. Answer text
            r'([a-d])\)\s*([^\n\r]+)'   # a) Answer text
        ]
        
        answers = []
        answer_letters = []
        
        for pattern in answer_patterns:
            matches = re.findall(pattern, answer_section)
            if len(matches) >= 2:  # Minimaal 2 antwoorden
                answer_letters = [m[0].upper() for m in matches]
                answers = [m[1].strip() for m in matches]
                break
        
        if len(answers) < 2:
            print(f"Skipping vraag {question_num}: onvoldoende antwoorden gevonden")
            continue
        
        # Zoek naar correcte antwoord
        correct_patterns = [
            r'(?:Correct\s*answer|Answer|Solution):\s*([A-Da-d])',
            r'(?:Antwoord|Oplossing):\s*([A-Da-d])',
            r'\b([A-Da-d])\s*is\s*correct',
            r'The\s*answer\s*is\s*([A-Da-d])'
        ]
        
        correct_indices = []
        for pattern in correct_patterns:
            matches = re.findall(pattern, answer_section, re.IGNORECASE)
            if matches:
                for match in matches:
                    correct_letter = match.upper()
                    if correct_letter in answer_letters:
                        correct_index = answer_letters.index(correct_letter)
                        if correct_index not in correct_indices:
                            correct_indices.append(correct_index)
                break
        
        # Als geen correct antwoord gevonden, gebruik eerste als default
        if not correct_indices:
            correct_indices = [0]
            print(f"Waarschuwing: geen correct antwoord gevonden voor vraag {question_num}, gebruik A")
        
        questions.append({
            "number": int(question_num),
            "question": question_text,
            "answers": answers[:4],  # Max 4 antwoorden
            "correct": correct_indices
        })
        
        print(f"✓ Vraag {question_num}: {question_text[:50]}... ({len(answers)} antwoorden)")
    
    return questions

def save_questions_to_file(questions, filename):
    """Save questions to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"Vragen opgeslagen in {filename}")

if __name__ == "__main__":
    # Extract questions from PDF
    pdf_path = "/root/quiz-app/PSPO1_v1.2.1.pdf"
    
    print("🔍 Extracting PSPO1 vragen uit PDF...")
    questions = extract_pspo_questions(pdf_path)
    
    print(f"\n=== RESULTAAT ===")
    print(f"✅ Gevonden: {len(questions)} vragen")
    
    # Save to JSON for review
    save_questions_to_file(questions, "/root/quiz-app/pspo1_questions.json")
    
    # Show first few questions for preview
    print(f"\n=== VOORBEELDEN ===")
    for i, q in enumerate(questions[:2]):
        print(f"\n--- Vraag {q['number']} ---")
        print(f"Tekst: {q['question']}")
        print(f"Antwoorden:")
        for j, ans in enumerate(q['answers']):
            marker = "✓" if j in q['correct'] else " "
            print(f"  {chr(65+j)}. {ans} {marker}")
        print(f"Correct: {[chr(65+i) for i in q['correct']]}")
    
    if len(questions) > 0:
        print(f"\n📁 Alle vragen opgeslagen in pspo1_questions.json")
        print(f"🎯 Volgende stap: toevoegen aan database als 'PSPO1' categorie")
    else:
        print("⚠️  Geen vragen gevonden - mogelijk ander PDF formaat")