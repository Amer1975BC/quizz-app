#!/usr/bin/env python3
"""
Database script om verpleegkundige rekenvragen toe te voegen
"""

import json
import psycopg2
from psycopg2.extras import RealDictCursor

def connect_to_db():
    """Verbind met de PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="quizdb", 
            user="quiz",
            password="quizpass_ChangeMe123",
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database verbinding mislukt: {e}")
        return None

def add_nursing_questions():
    """Voeg verpleegkundige rekenvragen toe aan database"""
    
    # Laad de gegenereerde vragen
    try:
        with open('verpleegkundige_rekenvragen.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except FileNotFoundError:
        print("❌ verpleegkundige_rekenvragen.json niet gevonden!")
        return
    
    conn = connect_to_db()
    if not conn:
        return
        
    cursor = conn.cursor()
    
    try:
        added_count = 0
        
        for i, q in enumerate(questions):
            # Voeg vraag toe aan questions tabel
            cursor.execute("""
                INSERT INTO questions (text, explanation, difficulty) 
                VALUES (%s, %s, %s) RETURNING id
            """, (q['text'], q['explanation'], q['difficulty']))
            
            question_id = cursor.fetchone()['id']
            
            # Voeg antwoordkeuzes toe
            for j, choice_text in enumerate(q['choices']):
                is_correct = j in q.get('correct_answers', [0])  # Default first answer correct
                
                cursor.execute("""
                    INSERT INTO choices (question_id, text, is_correct) 
                    VALUES (%s, %s, %s)
                """, (question_id, choice_text, is_correct))
            
            added_count += 1
            
            if (i + 1) % 10 == 0:
                print(f"✅ {i + 1} verpleegkundige vragen toegevoegd...")
        
        # Commit alle wijzigingen
        conn.commit()
        print(f"🎉 Succesvol {added_count} verpleegkundige rekenvragen toegevoegd!")
        
        # Toon totaal aantal vragen per categorie
        cursor.execute("""
            SELECT explanation, COUNT(*) as count 
            FROM questions 
            GROUP BY explanation 
            ORDER BY count DESC
        """)
        
        results = cursor.fetchall()
        print("\n📊 Vragen per categorie:")
        for row in results:
            print(f"  • {row['explanation']}: {row['count']} vragen")
            
    except Exception as e:
        print(f"❌ Error bij toevoegen vragen: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("🏥 Verpleegkundige rekenvragen toevoegen aan database...")
    add_nursing_questions()