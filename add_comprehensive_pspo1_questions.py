#!/usr/bin/env python3
"""
Add comprehensive PSPO1 questions to database
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection
DATABASE_URL = "postgresql+psycopg2://quiz:quizpass_ChangeMe123@localhost:5432/quizdb"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "quizdb"
DB_USER = "quiz"
DB_PASSWORD = "quizpass_ChangeMe123"

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def add_pspo1_questions():
    """Add comprehensive PSPO1 questions"""
    
    # Comprehensive PSPO1 questions based on certification material
    questions = [
        # Scrum Theory & Values
        {
            "text": "Which of the following are Scrum Values?",
            "choices": ["Commitment, Courage, Focus, Openness, Respect", "Transparency, Inspection, Adaptation", "Planning, Estimation, Review", "Analysis, Design, Implementation"],
            "correct": [0],
            "explanation": "PSPO1"
        },
        {
            "text": "What is the maximum length of a Sprint in Scrum?",
            "choices": ["1 month", "2 months", "3 months", "No maximum defined"],
            "correct": [0],
            "explanation": "PSPO1"
        },
        {
            "text": "True or False: Self-management means that the team can decide which Scrum events are needed.",
            "choices": ["True", "False"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        
        # Product Owner Role
        {
            "text": "Who is responsible for managing the Product Backlog?",
            "choices": ["The Scrum Master", "The Product Owner", "The Development Team", "The entire Scrum Team"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        {
            "text": "What are the Product Owner's responsibilities regarding the Product Backlog? (Choose all that apply)",
            "choices": ["Clearly expressing Product Backlog items", "Ordering the items in the Product Backlog", "Optimizing the value of the work the Development Team performs", "Ensuring the Product Backlog is visible, transparent, and clear"],
            "correct": [0, 1, 2, 3],
            "explanation": "PSPO1"
        },
        {
            "text": "True or False: The Product Owner may be part of the Development Team.",
            "choices": ["True", "False"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        
        # Product Backlog Management
        {
            "text": "What is the purpose of a Product Backlog?",
            "choices": ["To list all features that will ever be developed", "To provide a detailed plan for the next release", "To serve as a single source of requirements for any changes to be made to the product", "To document all defects found during testing"],
            "correct": [2],
            "explanation": "PSPO1"
        },
        {
            "text": "Who can add items to the Product Backlog?",
            "choices": ["Only the Product Owner", "Only the Scrum Master", "Anyone, but the Product Owner remains accountable", "Only the Development Team"],
            "correct": [2],
            "explanation": "PSPO1"
        },
        {
            "text": "What is Product Backlog refinement?",
            "choices": ["A Sprint event that happens at the end of the Sprint", "The act of breaking down and further defining Product Backlog items", "A meeting where only the Product Owner participates", "The process of removing old items from the Product Backlog"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        
        # Sprint Planning & Goals
        {
            "text": "Who creates the Sprint Goal?",
            "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "The Scrum Team"],
            "correct": [3],
            "explanation": "PSPO1"
        },
        {
            "text": "What is the purpose of the Sprint Goal?",
            "choices": ["To provide guidance to the Development Team on why it is building the increment", "To define exactly what will be delivered", "To ensure all Product Backlog items are completed", "To prevent any changes during the Sprint"],
            "correct": [0],
            "explanation": "PSPO1"
        },
        {
            "text": "True or False: The Product Owner must be present during Sprint Planning.",
            "choices": ["True", "False"],
            "correct": [0],
            "explanation": "PSPO1"
        },
        
        # Increment & Definition of Done
        {
            "text": "What is an Increment in Scrum?",
            "choices": ["A plan for the next Sprint", "The sum of all Product Backlog items completed during a Sprint", "A meeting to inspect the product", "The sum of all completed and valuable Product Backlog items since the beginning of the project"],
            "correct": [3],
            "explanation": "PSPO1"
        },
        {
            "text": "Who is responsible for the Definition of Done?",
            "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "The organization or the Scrum Team if not defined by the organization"],
            "correct": [3],
            "explanation": "PSPO1"
        },
        {
            "text": "True or False: An Increment must be released to production at the end of each Sprint.",
            "choices": ["True", "False"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        
        # Sprint Review & Stakeholders
        {
            "text": "What is the purpose of the Sprint Review?",
            "choices": ["To demonstrate completed work to stakeholders", "To inspect the Increment and adapt the Product Backlog if needed", "To plan the next Sprint", "To review the team's performance"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        {
            "text": "Who should attend the Sprint Review?",
            "choices": ["Only the Scrum Team", "The Scrum Team and key stakeholders", "Only the Product Owner and stakeholders", "The entire organization"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        {
            "text": "What is the maximum duration of a Sprint Review for a one-month Sprint?",
            "choices": ["2 hours", "4 hours", "8 hours", "1 day"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        
        # Value & ROI
        {
            "text": "What should guide the Product Owner in ordering the Product Backlog?",
            "choices": ["The technical complexity of items", "The size of the Development Team", "The value delivered to customers and stakeholders", "The alphabetical order of features"],
            "correct": [2],
            "explanation": "PSPO1"
        },
        {
            "text": "True or False: The value delivered by a product can only be determined by revenue.",
            "choices": ["True", "False"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        {
            "text": "When should a Product Owner consider canceling a Sprint?",
            "choices": ["When the Sprint Goal becomes obsolete", "When the Development Team is not working fast enough", "When stakeholders are not satisfied", "Never, Sprints should never be canceled"],
            "correct": [0],
            "explanation": "PSPO1"
        }
    ]
    
    # Additional advanced PSPO1 questions
    advanced_questions = [
        {
            "text": "What variables should a Product Owner consider when ordering the Product Backlog?",
            "choices": ["Value, risk, dependencies, and learning opportunities", "Only business value", "Technical difficulty only", "Team preferences"],
            "correct": [0],
            "explanation": "PSPO1"
        },
        {
            "text": "True or False: The Product Owner is accountable for maximizing the value of the product.",
            "choices": ["True", "False"],
            "correct": [0],
            "explanation": "PSPO1"
        },
        {
            "text": "Who determines when to release the product Increment?",
            "choices": ["The Scrum Master", "The Development Team", "The Product Owner", "The stakeholders"],
            "correct": [2],
            "explanation": "PSPO1"
        },
        {
            "text": "What is the role of stakeholders in Scrum?",
            "choices": ["They are part of the Scrum Team", "They provide input and feedback during Sprint Reviews", "They make all product decisions", "They manage the Development Team"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        {
            "text": "True or False: Product Backlog items must have estimates before they can be selected for a Sprint.",
            "choices": ["True", "False"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        {
            "text": "What is the relationship between the Product Owner and stakeholders?",
            "choices": ["The Product Owner reports to stakeholders", "Stakeholders are customers of the Product Owner's work", "The Product Owner manages stakeholders", "There is no relationship"],
            "correct": [1],
            "explanation": "PSPO1"
        },
        {
            "text": "When does the Development Team participate in Product Backlog refinement?",
            "choices": ["Only during Sprint Planning", "During dedicated refinement meetings", "Ongoing throughout the Sprint", "Never"],
            "correct": [2],
            "explanation": "PSPO1"
        },
        {
            "text": "True or False: The Product Owner can delegate writing Product Backlog items to others.",
            "choices": ["True", "False"],
            "correct": [0],
            "explanation": "PSPO1"
        },
        {
            "text": "What happens when a Product Backlog item cannot be completed within one Sprint?",
            "choices": ["The Sprint is extended", "The item is removed from the Sprint", "The item is broken down into smaller items", "The Definition of Done is changed"],
            "correct": [2],
            "explanation": "PSPO1"
        },
        {
            "text": "Who is responsible for tracking progress toward the Sprint Goal?",
            "choices": ["The Product Owner", "The Scrum Master", "The Development Team", "All of the above"],
            "correct": [2],
            "explanation": "PSPO1"
        }
    ]
    
    # Combine all questions
    all_questions = questions + advanced_questions
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        added_count = 0
        
        for question_data in all_questions:
            # Insert question
            cursor.execute("""
                INSERT INTO questions (text, explanation, difficulty) 
                VALUES (%s, %s, 'medium') 
                RETURNING id
            """, (question_data["text"], question_data["explanation"]))
            
            question_id = cursor.fetchone()[0]
            
            # Insert choices
            for i, choice_text in enumerate(question_data["choices"]):
                is_correct = i in question_data["correct"]
                cursor.execute("""
                    INSERT INTO choices (question_id, text, is_correct)
                    VALUES (%s, %s, %s)
                """, (question_id, choice_text, is_correct))
            
            added_count += 1
            
        conn.commit()
        print(f"✅ Successfully added {added_count} PSPO1 questions to database!")
        
        # Show current question count
        cursor.execute("SELECT COUNT(*) FROM questions WHERE explanation = 'PSPO1'")
        total_pspo1 = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM questions")
        total_questions = cursor.fetchone()[0]
        
        print(f"📊 Database now contains:")
        print(f"   • PSPO1 questions: {total_pspo1}")
        print(f"   • Total questions: {total_questions}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error adding questions: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_pspo1_questions()