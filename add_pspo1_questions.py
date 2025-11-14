import json
import psycopg2

# PSPO1 sample questions based on the PDF structure I can see
pspo1_questions = [
    {
        "question": "True or False: The Sprint Review is the only time at which stakeholder feedback is taken into account.",
        "answers": ["True", "False"],
        "correct": [1]  # False
    },
    {
        "question": "True or False: The value delivered by a product can only be determined by revenue.",
        "answers": ["True", "False"], 
        "correct": [1]  # False
    },
    {
        "question": "When can the Product Backlog be updated?",
        "answers": [
            "Only during Sprint Planning",
            "At any time by the Product Owner",
            "Only during the Sprint Review",
            "Only between Sprints"
        ],
        "correct": [1]
    },
    {
        "question": "True or False: The Product Owner should have the entire Product Backlog documented in detail before the first Sprint can start?",
        "answers": ["True", "False"],
        "correct": [1]  # False
    },
    {
        "question": "True or False: The Sprint Backlog is a result of Sprint Planning, and it includes the Sprint Goal.",
        "answers": ["True", "False"],
        "correct": [0]  # True
    },
    {
        "question": "Who is accountable for creating a valuable and usable Increment each Sprint?",
        "answers": [
            "The Product Owner",
            "The Scrum Master", 
            "The Developers",
            "The entire Scrum Team"
        ],
        "correct": [2]  # The Developers
    },
    {
        "question": "How much time must a Product Owner spend with the Developers?",
        "answers": [
            "40% of their time",
            "At least 50% of their time",
            "As much time as needed for the Developers to be successful",
            "All of their time"
        ],
        "correct": [2]
    },
    {
        "question": "True or False: All planned work for the Product done by the Scrum Team must originate from the Product Backlog.",
        "answers": ["True", "False"],
        "correct": [0]  # True
    },
    {
        "question": "Which of the following are Scrum Values?",
        "answers": [
            "Commitment, Courage, Focus, Openness, Respect",
            "Quality, Innovation, Speed, Efficiency",
            "Planning, Execution, Review, Adaptation", 
            "Leadership, Teamwork, Communication, Trust"
        ],
        "correct": [0]
    },
    {
        "question": "What variables should a Product Owner consider when ordering the Product Backlog?",
        "answers": [
            "Value, dependencies, size, and urgency",
            "Only business value",
            "Technical complexity only",
            "Stakeholder preferences only"
        ],
        "correct": [0]
    },
    {
        "question": "True or False: Dependencies could influence how the Product Owner orders Product Backlog Items.",
        "answers": ["True", "False"],
        "correct": [0]  # True
    },
    {
        "question": "A Product Backlog is: (choose the best three answers)",
        "answers": [
            "An ordered list of everything needed in the product",
            "Never complete",
            "Dynamic and evolving",
            "Fixed once created"
        ],
        "correct": [0, 1, 2]  # Multiple correct answers
    },
    {
        "question": "How often should customer satisfaction be measured?",
        "answers": [
            "Once per Sprint",
            "Frequently",
            "Once per release",
            "Annually"
        ],
        "correct": [1]
    },
    {
        "question": "What is the responsibility of the Product Owner in crafting the Sprint Goal?",
        "answers": [
            "The Product Owner creates the Sprint Goal alone",
            "The Product Owner collaborates with the Developers to craft the Sprint Goal",
            "The Scrum Master creates the Sprint Goal",
            "The Sprint Goal is not needed"
        ],
        "correct": [1]
    },
    {
        "question": "True or False: The Product Owner must write all of the Product Backlog Items before handing them over to the Scrum Team.",
        "answers": ["True", "False"],
        "correct": [1]  # False
    }
]

def connect_to_database():
    """Connect to PostgreSQL database"""
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
        print(f"Database connection error: {e}")
        return None

def add_pspo1_questions_to_db():
    """Add PSPO1 questions to database with category"""
    conn = connect_to_database()
    if not conn:
        return
    
    cursor = conn.cursor()
    added_count = 0
    
    for i, q in enumerate(pspo1_questions, 1):
        try:
            # Insert question with category/explanation marking it as PSPO1
            cursor.execute("""
                INSERT INTO questions (text, explanation, difficulty) 
                VALUES (%s, %s, %s) RETURNING id
            """, (q["question"], "PSPO1", 2))  # Use explanation field for category
            
            question_id = cursor.fetchone()[0]
            
            # Insert choices
            for j, answer in enumerate(q["answers"]):
                is_correct = j in q["correct"]
                cursor.execute("""
                    INSERT INTO choices (question_id, text, is_correct)
                    VALUES (%s, %s, %s)
                """, (question_id, answer, is_correct))
            
            added_count += 1
            print(f"✓ PSPO1 Vraag {i} toegevoegd: {q['question'][:60]}...")
            
        except Exception as e:
            print(f"✗ Fout bij vraag {i}: {str(e)}")
            conn.rollback()
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n=== PSPO1 RESULTAAT ===")
    print(f"✅ Succesvol toegevoegd: {added_count} PSPO1 vragen")
    return added_count

if __name__ == "__main__":
    print("🎯 Adding PSPO1 questions to database...")
    
    # Save questions to JSON for backup
    with open("/app/pspo1_sample_questions.json", 'w', encoding='utf-8') as f:
        json.dump(pspo1_questions, f, indent=2, ensure_ascii=False)
    
    count = add_pspo1_questions_to_db()
    
    print(f"\n📁 Sample vragen ook opgeslagen in pspo1_sample_questions.json")
    print(f"🎯 Volgende stap: voeg quiz selector toe aan frontend")
    print(f"💡 Je kunt meer PSPO1 vragen toevoegen via de admin interface")