import json
import random
import psycopg2
import os

def generate_quiz_questions():
    """Genereert 100 quiz vragen met 4 antwoordmogelijkheden"""
    
    # 80 vragen met 1 correct antwoord
    single_answer_questions = [
        {"question": "Wat is de hoofdstad van Frankrijk?", "answers": ["Parijs", "Londen", "Berlijn", "Madrid"], "correct": [0]},
        {"question": "Hoeveel benen heeft een spin?", "answers": ["6", "8", "10", "12"], "correct": [1]},
        {"question": "Welke planeet staat het dichtst bij de zon?", "answers": ["Venus", "Mercurius", "Aarde", "Mars"], "correct": [1]},
        {"question": "Wat is 15 + 27?", "answers": ["40", "42", "45", "48"], "correct": [1]},
        {"question": "In welk jaar begon de Tweede Wereldoorlog?", "answers": ["1938", "1939", "1940", "1941"], "correct": [1]},
        {"question": "Wat is de chemische formule van water?", "answers": ["H2O", "CO2", "O2", "H2SO4"], "correct": [0]},
        {"question": "Wie schreef 'Romeo en Julia'?", "answers": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "correct": [1]},
        {"question": "Welke oceaan is de grootste?", "answers": ["Atlantische Oceaan", "Stille Oceaan", "Indische Oceaan", "Arctische Oceaan"], "correct": [1]},
        {"question": "Wat is 7 × 8?", "answers": ["54", "56", "58", "60"], "correct": [1]},
        {"question": "Welk gas ademen mensen in?", "answers": ["Zuurstof", "Koolstofdioxide", "Stikstof", "Waterstof"], "correct": [0]},
        {"question": "Hoeveel continenten zijn er?", "answers": ["5", "6", "7", "8"], "correct": [2]},
        {"question": "Wat is de grootste mammal ter wereld?", "answers": ["Olifant", "Blauwe walvis", "Giraffe", "Nijlpaard"], "correct": [1]},
        {"question": "Welke kleur krijg je door rood en blauw te mengen?", "answers": ["Groen", "Paars", "Oranje", "Geel"], "correct": [1]},
        {"question": "Hoeveel dagen heeft februari in een schrikkeljaar?", "answers": ["28", "29", "30", "31"], "correct": [1]},
        {"question": "Wat is de snelheid van het licht?", "answers": ["300.000 km/s", "150.000 km/s", "450.000 km/s", "600.000 km/s"], "correct": [0]},
        {"question": "Welke rivier stroomt door Londen?", "answers": ["Seine", "Rijn", "Theems", "Donau"], "correct": [2]},
        {"question": "Wat is √64?", "answers": ["6", "7", "8", "9"], "correct": [2]},
        {"question": "Wie schilderde de Mona Lisa?", "answers": ["Van Gogh", "Picasso", "Leonardo da Vinci", "Michelangelo"], "correct": [2]},
        {"question": "Hoeveel graden heeft een cirkel?", "answers": ["180", "270", "360", "450"], "correct": [2]},
        {"question": "Welk element heeft het symbool 'Au'?", "answers": ["Aluminium", "Goud", "Zilver", "Koper"], "correct": [1]},
        {"question": "In welk land staat de Eiffeltoren?", "answers": ["Italië", "Frankrijk", "Spanje", "Duitsland"], "correct": [1]},
        {"question": "Wat is 100 - 37?", "answers": ["61", "63", "65", "67"], "correct": [1]},
        {"question": "Welke maand heeft 30 dagen NIET?", "answers": ["April", "Juni", "September", "Februari"], "correct": [3]},
        {"question": "Wat is de hoofdstad van Australië?", "answers": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "correct": [2]},
        {"question": "Hoeveel strings heeft een standaard gitaar?", "answers": ["4", "5", "6", "7"], "correct": [2]},
        {"question": "Welke vorm heeft een voetbal?", "answers": ["Vierkant", "Driehoek", "Zeshoek en vijfhoek", "Cirkel"], "correct": [2]},
        {"question": "Wat is 12 × 12?", "answers": ["124", "134", "144", "154"], "correct": [2]},
        {"question": "Welke vogel kan niet vliegen?", "answers": ["Adelaar", "Pinguïn", "Kraai", "Duif"], "correct": [1]},
        {"question": "Hoeveel ogen heeft een mens normaal?", "answers": ["1", "2", "3", "4"], "correct": [1]},
        {"question": "Wat is de kleinste eenheid van materie?", "answers": ["Molecuul", "Atoom", "Electron", "Proton"], "correct": [1]},
        {"question": "Welke taal spreekt men in Brazilië?", "answers": ["Spaans", "Portugees", "Engels", "Frans"], "correct": [1]},
        {"question": "Hoeveel seconden zitten er in een minuut?", "answers": ["30", "45", "60", "90"], "correct": [2]},
        {"question": "Wat is de hoofdstad van Italië?", "answers": ["Milaan", "Napels", "Rome", "Venetië"], "correct": [2]},
        {"question": "Welk orgaan pompt bloed rond?", "answers": ["Lever", "Hart", "Longen", "Nieren"], "correct": [1]},
        {"question": "Wat is 25% van 200?", "answers": ["25", "50", "75", "100"], "correct": [1]},
        {"question": "Welke kleur heeft de zon?", "answers": ["Wit", "Geel", "Oranje", "Rood"], "correct": [1]},
        {"question": "Hoeveel minuten zitten er in een uur?", "answers": ["30", "45", "60", "90"], "correct": [2]},
        {"question": "Welk dier geeft melk?", "answers": ["Paard", "Koe", "Schaap", "Varken"], "correct": [1]},
        {"question": "Wat is 9 + 16?", "answers": ["23", "24", "25", "26"], "correct": [2]},
        {"question": "Welke seizoen komt na de winter?", "answers": ["Zomer", "Herfst", "Lente", "Winter"], "correct": [2]},
        {"question": "Hoeveel hoeken heeft een driehoek?", "answers": ["2", "3", "4", "5"], "correct": [1]},
        {"question": "Wat is de hoofdstad van Nederland?", "answers": ["Rotterdam", "Amsterdam", "Den Haag", "Utrecht"], "correct": [1]},
        {"question": "Welk metaal is vloeibaar bij kamertemperatuur?", "answers": ["IJzer", "Goud", "Kwik", "Zilver"], "correct": [2]},
        {"question": "Wat is 81 ÷ 9?", "answers": ["8", "9", "10", "11"], "correct": [1]},
        {"question": "Welke planeet heeft ringen?", "answers": ["Mars", "Venus", "Saturnus", "Neptunus"], "correct": [2]},
        {"question": "Hoeveel hersenhelften heeft een mens?", "answers": ["1", "2", "3", "4"], "correct": [1]},
        {"question": "Wat is de hoogste berg ter wereld?", "answers": ["K2", "Mount Everest", "Mont Blanc", "Kilimanjaro"], "correct": [1]},
        {"question": "Welke vorm heeft een dobbelsteen?", "answers": ["Kubus", "Cilinder", "Kegel", "Bol"], "correct": [0]},
        {"question": "Wat is 144 ÷ 12?", "answers": ["11", "12", "13", "14"], "correct": [1]},
        {"question": "Welke kleur ontstaat door geel en blauw te mengen?", "answers": ["Paars", "Oranje", "Groen", "Roze"], "correct": [2]},
        {"question": "Hoeveel werkdagen heeft een standaard werkweek?", "answers": ["4", "5", "6", "7"], "correct": [1]},
        {"question": "Wat is het tegenovergestelde van 'warm'?", "answers": ["Heet", "Koud", "Mild", "Lauw"], "correct": [1]},
        {"question": "Welk fruit is geel en gebogen?", "answers": ["Appel", "Banaan", "Sinaasappel", "Druif"], "correct": [1]},
        {"question": "Wat is 3³ (3 tot de macht 3)?", "answers": ["9", "18", "27", "81"], "correct": [2]},
        {"question": "Welke sport speelt men op Wimbledon?", "answers": ["Voetbal", "Tennis", "Cricket", "Rugby"], "correct": [1]},
        {"question": "Hoeveel cijfers heeft het getal 1000?", "answers": ["3", "4", "5", "6"], "correct": [1]},
        {"question": "Wat is de hoofdstad van Spanje?", "answers": ["Barcelona", "Madrid", "Sevilla", "Valencia"], "correct": [1]},
        {"question": "Welk gas produceren planten bij fotosynthese?", "answers": ["Koolstofdioxide", "Zuurstof", "Stikstof", "Waterstof"], "correct": [1]},
        {"question": "Wat is 20% van 150?", "answers": ["20", "25", "30", "35"], "correct": [2]},
        {"question": "Welke letter komt na 'M' in het alfabet?", "answers": ["L", "N", "O", "P"], "correct": [1]},
        {"question": "Hoeveel zijden heeft een hexagoon?", "answers": ["5", "6", "7", "8"], "correct": [1]},
        {"question": "Wat is het symbool voor natrium?", "answers": ["N", "Na", "Ni", "No"], "correct": [1]},
        {"question": "Welke maand heeft 31 dagen?", "answers": ["April", "Juni", "September", "Januari"], "correct": [3]},
        {"question": "Wat is 17 × 3?", "answers": ["49", "51", "53", "55"], "correct": [1]},
        {"question": "Welke kleur krijg je door alle kleuren te mengen?", "answers": ["Zwart", "Wit", "Grijs", "Bruin"], "correct": [0]},
        {"question": "Hoeveel hoeken heeft een vierkant?", "answers": ["3", "4", "5", "6"], "correct": [1]},
        {"question": "Wat is de kleinste oceaan?", "answers": ["Atlantische Oceaan", "Indische Oceaan", "Arctische Oceaan", "Stille Oceaan"], "correct": [2]},
        {"question": "Welk element heeft symbool 'O'?", "answers": ["Osmium", "Zuurstof", "Ozon", "Oxide"], "correct": [1]},
        {"question": "Wat is 99 + 1?", "answers": ["99", "100", "101", "102"], "correct": [1]},
        {"question": "Welke vorm heeft een ei?", "answers": ["Rond", "Vierkant", "Ovaal", "Driehoekig"], "correct": [2]},
        {"question": "Hoeveel tenen heeft een mens normaal?", "answers": ["8", "10", "12", "14"], "correct": [1]},
        {"question": "Wat is de hoofdstad van Duitsland?", "answers": ["München", "Hamburg", "Berlijn", "Keulen"], "correct": [2]},
        {"question": "Welk dier heeft een lange nek?", "answers": ["Olifant", "Giraffe", "Paard", "Zebra"], "correct": [1]},
        {"question": "Wat is 50 ÷ 10?", "answers": ["4", "5", "6", "7"], "correct": [1]},
        {"question": "Welke planeet is rood?", "answers": ["Venus", "Mars", "Jupiter", "Saturnus"], "correct": [1]},
        {"question": "Hoeveel poten heeft een tafel normaal?", "answers": ["2", "3", "4", "5"], "correct": [2]},
        {"question": "Wat is de hoofdstad van Canada?", "answers": ["Toronto", "Montreal", "Vancouver", "Ottawa"], "correct": [3]},
        {"question": "Welke kleur ontstaat door rood en geel te mengen?", "answers": ["Paars", "Groen", "Oranje", "Roze"], "correct": [2]},
        {"question": "Hoeveel maanden heeft een jaar?", "answers": ["10", "11", "12", "13"], "correct": [2]},
        {"question": "Wat is 6 × 7?", "answers": ["40", "42", "44", "46"], "correct": [1]},
        {"question": "Welk dier maakt honing?", "answers": ["Vlinder", "Bij", "Mier", "Wesp"], "correct": [1]},
        {"question": "Wat is de grootste planeet?", "answers": ["Aarde", "Jupiter", "Saturnus", "Neptunus"], "correct": [1]},
        {"question": "Hoeveel wielen heeft een auto normaal?", "answers": ["2", "3", "4", "6"], "correct": [2]},
        {"question": "Welke kleur heeft een banaan?", "answers": ["Rood", "Groen", "Geel", "Blauw"], "correct": [2]},
        {"question": "Wat is 200 ÷ 4?", "answers": ["40", "45", "50", "55"], "correct": [2]},
        {"question": "Welk seizoen is het koudst?", "answers": ["Lente", "Zomer", "Herfst", "Winter"], "correct": [3]}
    ]
    
    # 20 vragen met meerdere correcte antwoorden
    multiple_answer_questions = [
        {"question": "Welke van deze zijn primaire kleuren?", "answers": ["Rood", "Groen", "Blauw", "Geel"], "correct": [0, 2, 3]},
        {"question": "Welke getallen zijn even?", "answers": ["2", "3", "4", "5"], "correct": [0, 2]},
        {"question": "Welke dieren zijn zoogdieren?", "answers": ["Hond", "Vis", "Kat", "Vogel"], "correct": [0, 2]},
        {"question": "Welke van deze zijn continenten?", "answers": ["Europa", "Californië", "Azië", "Texas"], "correct": [0, 2]},
        {"question": "Welke getallen zijn deelbaar door 3?", "answers": ["6", "7", "9", "10"], "correct": [0, 2]},
        {"question": "Welke van deze zijn hoofdsteden?", "answers": ["Londen", "Manchester", "Parijs", "Liverpool"], "correct": [0, 2]},
        {"question": "Welke planeten hebben manen?", "answers": ["Aarde", "Venus", "Jupiter", "Mercurius"], "correct": [0, 2]},
        {"question": "Welke vormen hebben rechte hoeken?", "answers": ["Vierkant", "Cirkel", "Rechthoek", "Driehoek"], "correct": [0, 2]},
        {"question": "Welke van deze zijn metalen?", "answers": ["IJzer", "Plastic", "Goud", "Hout"], "correct": [0, 2]},
        {"question": "Welke maanden hebben 31 dagen?", "answers": ["Januari", "Februari", "Maart", "April"], "correct": [0, 2]},
        {"question": "Welke dieren leven in water?", "answers": ["Vis", "Paard", "Dolfijn", "Kat"], "correct": [0, 2]},
        {"question": "Welke getallen zijn groter dan 5?", "answers": ["3", "7", "4", "8"], "correct": [1, 3]},
        {"question": "Welke van deze zijn vruchten?", "answers": ["Appel", "Wortel", "Banaan", "Ui"], "correct": [0, 2]},
        {"question": "Welke kleuren zie je in een regenboog?", "answers": ["Rood", "Zwart", "Blauw", "Wit"], "correct": [0, 2]},
        {"question": "Welke organen zitten in je hoofd?", "answers": ["Hersenen", "Hart", "Ogen", "Lever"], "correct": [0, 2]},
        {"question": "Welke van deze zijn instrumenten?", "answers": ["Piano", "Stoel", "Gitaar", "Tafel"], "correct": [0, 2]},
        {"question": "Welke seizoenen zijn warm?", "answers": ["Winter", "Lente", "Zomer", "Herfst"], "correct": [1, 2]},
        {"question": "Welke getallen zijn oneven?", "answers": ["1", "2", "3", "4"], "correct": [0, 2]},
        {"question": "Welke van deze zijn vogels?", "answers": ["Adelaar", "Hond", "Mus", "Kat"], "correct": [0, 2]},
        {"question": "Welke van deze zijn landen in Europa?", "answers": ["Frankrijk", "Japan", "Italië", "China"], "correct": [0, 2]}
    ]
    
    # Combineer de lijsten
    questions = single_answer_questions + multiple_answer_questions
    
    # Schud de vragen
    random.shuffle(questions)
    
    return questions[:100]

def connect_to_database():
    """Verbind met PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host="postgres",
            port="5432",
            database="quizdb",
            user="quiz",
            password="quizpass_ChangeMe123"
        )
        return conn
    except Exception as e:
        print(f"Fout bij database verbinding: {e}")
        return None

def add_questions_to_database(questions):
    """Voegt vragen toe aan de database"""
    conn = connect_to_database()
    if not conn:
        print("Kan niet verbinden met database")
        return
    
    cursor = conn.cursor()
    added_count = 0
    failed_count = 0
    
    for i, q in enumerate(questions, 1):
        try:
            # Insert question into questions table
            cursor.execute("""
                INSERT INTO questions (text, difficulty) 
                VALUES (%s, %s) RETURNING id
            """, (q["question"], 1))
            
            question_id = cursor.fetchone()[0]
            
            # Insert choices for this question
            for j, answer in enumerate(q["answers"]):
                is_correct = j in q["correct"]
                cursor.execute("""
                    INSERT INTO choices (question_id, text, is_correct)
                    VALUES (%s, %s, %s)
                """, (question_id, answer, is_correct))
            
            added_count += 1
            print(f"✓ Vraag {i} toegevoegd: {q['question'][:50]}...")
            
        except Exception as e:
            failed_count += 1
            print(f"✗ Fout bij vraag {i}: {str(e)}")
            conn.rollback()  # Rollback on error
    
    # Commit changes
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n=== Resultaat ===")
    print(f"Succesvol toegevoegd: {added_count}")
    print(f"Gefaald: {failed_count}")
    print(f"Totaal: {len(questions)}")

if __name__ == "__main__":
    print("Genereren van 100 quiz vragen...")
    questions = generate_quiz_questions()
    
    print(f"\nGegenereerd: {len(questions)} vragen")
    print(f"Vragen met 1 antwoord: {sum(1 for q in questions if len(q['correct']) == 1)}")
    print(f"Vragen met meerdere antwoorden: {sum(1 for q in questions if len(q['correct']) > 1)}")
    
    print(f"\nToevoegen aan database...")
    add_questions_to_database(questions)