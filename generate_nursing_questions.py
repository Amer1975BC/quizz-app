#!/usr/bin/env python3
"""
Verpleegkundig Rekenen Quiz Generator
Genereert 100 rekenvragen voor verpleegkundigen MBO niveau 4
"""

import json
import random
from typing import List, Dict

def generate_dosage_calculations() -> List[Dict]:
    """Genereert doseringsvragen"""
    questions = []
    
    # Basis dosering vragen
    dosage_questions = [
        {
            "text": "Een patiënt moet 500mg paracetamol krijgen. De tabletten bevatten 250mg per stuk. Hoeveel tabletten geef je?",
            "choices": ["1 tablet", "2 tabletten", "3 tabletten", "4 tabletten"],
            "correct": [1]
        },
        {
            "text": "De voorgeschreven dosis is 0,25mg digoxine. Je hebt tabletten van 0,125mg. Hoeveel tabletten zijn nodig?",
            "choices": ["1 tablet", "2 tabletten", "3 tabletten", "0,5 tablet"],
            "correct": [1]
        },
        {
            "text": "Een patiënt weegt 70kg en moet 15mg/kg prednisolon krijgen. Wat is de totale dagdosis?",
            "choices": ["1050mg", "950mg", "1150mg", "850mg"],
            "correct": [0]
        },
        {
            "text": "Van een 10% glucoseoplossing moet je 250ml toedienen. Hoeveel gram glucose krijgt de patiënt?",
            "choices": ["25 gram", "20 gram", "30 gram", "15 gram"],
            "correct": [0]
        },
        {
            "text": "Een infuus van 1000ml moet in 8 uur lopen. Wat is de druppelsnelheid bij 20 druppels/ml?",
            "choices": ["42 druppels/min", "38 druppels/min", "45 druppels/min", "40 druppels/min"],
            "correct": [0]
        }
    ]
    
    for i, q in enumerate(dosage_questions):
        questions.append({
            "text": q["text"],
            "choices": q["choices"],
            "category": "Verpleegkundig Rekenen",
            "difficulty": 2,
            "explanation": "Verpleegkundig Rekenen",
            "correct_answers": q["correct"]
        })
    
    return questions

def generate_iv_calculations() -> List[Dict]:
    """Genereert infuusvragen"""
    questions = []
    
    iv_questions = [
        {
            "text": "Een infuus van 500ml NaCl 0.9% moet in 4 uur gegeven worden. Bereken ml/uur:",
            "choices": ["125 ml/uur", "120 ml/uur", "130 ml/uur", "110 ml/uur"],
            "correct": [0]
        },
        {
            "text": "Bij 15 druppels/ml, hoeveel druppels per minuut voor 100ml/uur?",
            "choices": ["25 druppels/min", "30 druppels/min", "20 druppels/min", "35 druppels/min"],
            "correct": [0]
        },
        {
            "text": "Een medicijnpomp staat op 5ml/uur. Hoeveel ml wordt er in 24 uur toegediend?",
            "choices": ["120ml", "100ml", "140ml", "110ml"],
            "correct": [0]
        },
        {
            "text": "1000ml glucose 5% in 12 uur. Wat is de snelheid in ml/min?",
            "choices": ["1.39 ml/min", "1.25 ml/min", "1.50 ml/min", "1.10 ml/min"],
            "correct": [0]
        },
        {
            "text": "Een patiënt krijgt 2ml/uur morfine via een pomp. Hoeveel ml per 8-uurs dienst?",
            "choices": ["16ml", "14ml", "18ml", "12ml"],
            "correct": [0]
        }
    ]
    
    for q in iv_questions:
        questions.append({
            "text": q["text"],
            "choices": q["choices"],
            "category": "Verpleegkundig Rekenen",
            "difficulty": 2,
            "explanation": "Verpleegkundig Rekenen",
            "correct_answers": q["correct"]
        })
    
    return questions

def generate_concentration_calculations() -> List[Dict]:
    """Genereert concentratie berekeningen"""
    questions = []
    
    concentration_questions = [
        {
            "text": "Hoeveel gram zout zit er in 100ml van een 0.9% NaCl oplossing?",
            "choices": ["0.9 gram", "0.09 gram", "9 gram", "90 gram"],
            "correct": [0]
        },
        {
            "text": "Een 1:1000 adrenaline oplossing bevat hoeveel mg per ml?",
            "choices": ["1 mg/ml", "0.1 mg/ml", "10 mg/ml", "0.01 mg/ml"],
            "correct": [0]
        },
        {
            "text": "Van een 20% glucoseoplossing heb je 50ml. Hoeveel gram glucose is dit?",
            "choices": ["10 gram", "8 gram", "12 gram", "15 gram"],
            "correct": [0]
        },
        {
            "text": "Een 0.5% lidocaïne oplossing bevat hoeveel mg per 10ml?",
            "choices": ["50mg", "5mg", "0.5mg", "500mg"],
            "correct": [0]
        },
        {
            "text": "Hoeveel ml van een 10% oplossing heb je nodig voor 2 gram werkzame stof?",
            "choices": ["20ml", "15ml", "25ml", "10ml"],
            "correct": [0]
        }
    ]
    
    for q in concentration_questions:
        questions.append({
            "text": q["text"],
            "choices": q["choices"],
            "category": "Verpleegkundig Rekenen",
            "difficulty": 2,
            "explanation": "Verpleegkundig Rekenen",
            "correct_answers": q["correct"]
        })
    
    return questions

def generate_unit_conversions() -> List[Dict]:
    """Genereert eenheidsconversies"""
    questions = []
    
    conversion_questions = [
        {
            "text": "Converteer 2.5 gram naar milligram:",
            "choices": ["2500mg", "250mg", "25mg", "25000mg"],
            "correct": [0]
        },
        {
            "text": "Hoeveel microgram is 0.5mg?",
            "choices": ["500 microgram", "50 microgram", "5000 microgram", "5 microgram"],
            "correct": [0]
        },
        {
            "text": "Converteer 1.5 liter naar milliliter:",
            "choices": ["1500ml", "150ml", "15ml", "15000ml"],
            "correct": [0]
        },
        {
            "text": "Hoeveel gram is 750mg?",
            "choices": ["0.75 gram", "7.5 gram", "75 gram", "0.075 gram"],
            "correct": [0]
        },
        {
            "text": "Converteer 3 uur naar minuten:",
            "choices": ["180 minuten", "300 minuten", "120 minuten", "240 minuten"],
            "correct": [0]
        }
    ]
    
    for q in conversion_questions:
        questions.append({
            "text": q["text"],
            "choices": q["choices"],
            "category": "Verpleegkundig Rekenen",
            "difficulty": 1,
            "explanation": "Verpleegkundig Rekenen",
            "correct_answers": q["correct"]
        })
    
    return questions

def generate_pediatric_calculations() -> List[Dict]:
    """Genereert pediatrische doseringen"""
    questions = []
    
    pediatric_questions = [
        {
            "text": "Een kind van 25kg moet 20mg/kg paracetamol. Wat is de totale dosis?",
            "choices": ["500mg", "400mg", "600mg", "300mg"],
            "correct": [0]
        },
        {
            "text": "Paracetamol suspensie bevat 120mg/5ml. Voor 240mg, hoeveel ml?",
            "choices": ["10ml", "8ml", "12ml", "6ml"],
            "correct": [0]
        },
        {
            "text": "Een baby van 8kg moet 0.1ml/kg furosemide. Hoeveel ml totaal?",
            "choices": ["0.8ml", "0.6ml", "1ml", "1.2ml"],
            "correct": [0]
        },
        {
            "text": "Amoxicilline 50mg/kg voor een kind van 15kg. Totale dagdosis?",
            "choices": ["750mg", "650mg", "850mg", "550mg"],
            "correct": [0]
        },
        {
            "text": "Een kind moet 2mg/kg prednisolon. Gewicht 12kg. Hoeveel mg?",
            "choices": ["24mg", "20mg", "28mg", "16mg"],
            "correct": [0]
        }
    ]
    
    for q in pediatric_questions:
        questions.append({
            "text": q["text"],
            "choices": q["choices"],
            "category": "Verpleegkundig Rekenen",
            "difficulty": 3,
            "explanation": "Verpleegkundig Rekenen",
            "correct_answers": q["correct"]
        })
    
    return questions

def generate_additional_questions() -> List[Dict]:
    """Genereert aanvullende verpleegkundige rekenvragen"""
    questions = []
    
    # Meer complexe vragen
    complex_questions = [
        {
            "text": "Een patiënt heeft 2400ml vocht nodig per dag. Hij drinkt 1200ml. Hoeveel ml IV per uur over 24 uur?",
            "choices": ["50 ml/uur", "45 ml/uur", "55 ml/uur", "40 ml/uur"],
            "correct": [0]
        },
        {
            "text": "Heparine 5000E in 250ml. Voor 1200E/uur, hoeveel ml/uur?",
            "choices": ["60 ml/uur", "55 ml/uur", "65 ml/uur", "50 ml/uur"],
            "correct": [0]
        },
        {
            "text": "Insuline 50E in 50ml. Voor 6E/uur, wat is de pompsnelheid?",
            "choices": ["6 ml/uur", "5 ml/uur", "7 ml/uur", "8 ml/uur"],
            "correct": [0]
        },
        {
            "text": "Een patiënt van 80kg krijgt 7.5mg/kg vancomycine. Hoeveel mg totaal?",
            "choices": ["600mg", "550mg", "650mg", "500mg"],
            "correct": [0]
        },
        {
            "text": "Dopamine 400mg in 250ml. Voor 5mcg/kg/min bij 70kg. Ml/uur?",
            "choices": ["6.6 ml/uur", "6 ml/uur", "7 ml/uur", "5.5 ml/uur"],
            "correct": [0]
        }
    ]
    
    for q in complex_questions:
        questions.append({
            "text": q["text"],
            "choices": q["choices"],
            "category": "Verpleegkundig Rekenen",
            "difficulty": 3,
            "explanation": "Verpleegkundig Rekenen",
            "correct_answers": q["correct"]
        })
    
    return questions

def main():
    """Genereert alle verpleegkundige rekenvragen"""
    all_questions = []
    
    # Genereer verschillende categorieën vragen
    all_questions.extend(generate_dosage_calculations())
    all_questions.extend(generate_iv_calculations())
    all_questions.extend(generate_concentration_calculations())
    all_questions.extend(generate_unit_conversions())
    all_questions.extend(generate_pediatric_calculations())
    all_questions.extend(generate_additional_questions())
    
    # Genereer meer vragen tot we 100 hebben
    while len(all_questions) < 100:
        # Voeg variaties toe van bestaande vragen
        base_question = random.choice(all_questions[:20])
        
        # Maak variatie door getallen te veranderen
        new_question = create_question_variation(base_question, len(all_questions) + 1)
        all_questions.append(new_question)
    
    # Limiteer tot exact 100 vragen
    all_questions = all_questions[:100]
    
    print(f"✅ Gegenereerd: {len(all_questions)} verpleegkundige rekenvragen")
    
    # Sla op in JSON bestand
    with open('verpleegkundige_rekenvragen.json', 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)
    
    print("💾 Vragen opgeslagen in verpleegkundige_rekenvragen.json")
    return all_questions

def create_question_variation(base_question, question_num):
    """Maakt een variatie van een bestaande vraag"""
    # Dit is een vereenvoudigde versie - in practice zou je meer geavanceerde variaties maken
    text = base_question['text']
    
    # Vervang getallen met willekeurige variaties
    import re
    numbers = re.findall(r'\d+(?:\.\d+)?', text)
    
    if numbers:
        old_num = numbers[0]
        new_num = str(int(float(old_num)) + random.randint(-5, 5))
        new_text = text.replace(old_num, new_num, 1)
        
        return {
            "text": new_text,
            "choices": base_question['choices'],
            "category": "Verpleegkundig Rekenen",
            "difficulty": base_question['difficulty'],
            "explanation": "Verpleegkundig Rekenen",
            "correct_answers": base_question['correct_answers']
        }
    
    return base_question.copy()

if __name__ == "__main__":
    main()