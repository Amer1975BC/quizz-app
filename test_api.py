import pytest
import sys
import os
from pathlib import Path

# Add the parent directory to the Python path so we can import from webapi
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from webapi import app, SessionLocal, Question
from sqlalchemy import text
import json

# Test client for FastAPI
client = TestClient(app)

@pytest.fixture
def test_db():
    """Setup test database with known data"""
    db = SessionLocal()
    try:
        # Check if we have test data
        general_count = db.execute(text("SELECT COUNT(*) FROM questions WHERE explanation IS NULL")).scalar()
        pspo1_count = db.execute(text("SELECT COUNT(*) FROM questions WHERE explanation = 'PSPO1'")).scalar()
        nursing_count = db.execute(text("SELECT COUNT(*) FROM questions WHERE explanation = 'Verpleegkundig Rekenen'")).scalar()
        
        assert general_count > 0, "No general questions found in database"
        assert pspo1_count > 0, "No PSPO1 questions found in database"  
        assert nursing_count > 0, "No nursing questions found in database"
        
        yield db
    finally:
        db.close()

class TestQuizAPI:
    """Test suite for Quiz API endpoints"""
    
    def test_root_endpoint(self):
        """Test that root endpoint returns the quiz interface"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Quiz App" in response.text
    
    def test_static_files_serve(self):
        """Test that static files are served correctly"""
        response = client.get("/static/app.js")
        assert response.status_code == 200
        assert "application/javascript" in response.headers["content-type"]
        
        response = client.get("/static/styles.css")
        assert response.status_code == 200
        assert "text/css" in response.headers["content-type"]

class TestCategoryFiltering:
    """Test suite for strict category separation"""
    
    def test_general_quiz_start(self, test_db):
        """Test starting general quiz returns valid session"""
        response = client.post("/api/start?category=general")
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data
        assert data["category"] == "general"
        assert len(data["session_id"]) > 0
    
    def test_pspo1_quiz_start(self, test_db):
        """Test starting PSPO1 quiz returns valid session"""
        response = client.post("/api/start?category=PSPO1")
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data
        assert data["category"] == "PSPO1"
    
    def test_nursing_quiz_start(self, test_db):
        """Test starting nursing quiz returns valid session"""
        response = client.post("/api/start?category=Verpleegkundig Rekenen")
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data
        assert data["category"] == "Verpleegkundig Rekenen"
    
    def test_general_quiz_only_general_questions(self, test_db):
        """Test that general quiz only returns general questions"""
        # Start general quiz
        response = client.post("/api/start?category=general")
        session_id = response.json()["session_id"]
        
        # Get multiple questions to verify category consistency
        questions_checked = 0
        for _ in range(5):
            response = client.get(f"/api/question?sid={session_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get("finished"):
                    break
                    
                # Verify it's a general question by checking it's not PSPO1 or nursing specific
                question_text = data["question"]["text"]
                
                # PSPO1 questions typically contain Scrum terminology
                scrum_terms = ["scrum", "sprint", "product owner", "scrum master", "backlog", "development team"]
                is_likely_pspo1 = any(term.lower() in question_text.lower() for term in scrum_terms)
                
                # Nursing questions typically contain medical/calculation terminology  
                nursing_terms = ["mg", "ml", "oplossing", "medicijn", "dosering", "infuus"]
                is_likely_nursing = any(term.lower() in question_text.lower() for term in nursing_terms)
                
                # General questions should not contain specific domain terms
                assert not is_likely_pspo1, f"General quiz contains PSPO1-like question: {question_text[:80]}"
                assert not is_likely_nursing, f"General quiz contains nursing-like question: {question_text[:80]}"
                
                questions_checked += 1
                
                # Submit dummy answer to continue
                client.post(f"/api/answer?sid={session_id}", json={"choice": 0})
            
        assert questions_checked > 0, "No questions were checked for general quiz"
    
    def test_pspo1_quiz_only_pspo1_questions(self, test_db):
        """Test that PSPO1 quiz only returns PSPO1 questions"""
        # Start PSPO1 quiz
        response = client.post("/api/start?category=PSPO1")
        session_id = response.json()["session_id"]
        
        # Get first question and verify it's PSPO1 related
        response = client.get(f"/api/question?sid={session_id}")
        assert response.status_code == 200
        
        data = response.json()
        if not data.get("finished"):
            question_text = data["question"]["text"]
            
            # PSPO1 questions should contain Scrum-related terminology
            scrum_terms = ["scrum", "sprint", "product", "backlog", "development", "owner", "master", "team"]
            contains_scrum_terms = any(term.lower() in question_text.lower() for term in scrum_terms)
            
            assert contains_scrum_terms, f"PSPO1 quiz contains non-Scrum question: {question_text}"
    
    def test_nursing_quiz_only_nursing_questions(self, test_db):
        """Test that nursing quiz only returns nursing questions"""
        # Start nursing quiz
        response = client.post("/api/start?category=Verpleegkundig Rekenen")
        session_id = response.json()["session_id"]
        
        # Get first question and verify it's nursing related
        response = client.get(f"/api/question?sid={session_id}")
        assert response.status_code == 200
        
        data = response.json()
        if not data.get("finished"):
            question_text = data["question"]["text"]
            
            # Nursing questions should contain medical/calculation terminology
            nursing_terms = ["mg", "ml", "gram", "liter", "dosering", "medicijn", "oplossing", "infuus", "%"]
            contains_nursing_terms = any(term in question_text for term in nursing_terms)
            
            assert contains_nursing_terms, f"Nursing quiz contains non-medical question: {question_text}"

class TestQuestionFlow:
    """Test suite for question flow and answers"""
    
    def test_question_structure(self, test_db):
        """Test that questions have correct structure"""
        response = client.post("/api/start?category=general")
        session_id = response.json()["session_id"]
        
        response = client.get(f"/api/question?sid={session_id}")
        assert response.status_code == 200
        
        data = response.json()
        if not data.get("finished"):
            question = data["question"]
            
            # Verify question structure
            assert "text" in question
            assert "choices" in question
            assert "correct_answers" in question
            assert len(question["choices"]) >= 2  # At least 2 choices
            assert len(question["text"]) > 0  # Non-empty question text
            
            # Verify answer is not exposed in question response
            assert "answer" not in question
    
    def test_answer_submission(self, test_db):
        """Test answer submission and scoring"""
        response = client.post("/api/start?category=general")
        session_id = response.json()["session_id"]
        
        # Get question
        response = client.get(f"/api/question?sid={session_id}")
        data = response.json()
        
        if not data.get("finished"):
            # Submit answer
            response = client.post(f"/api/answer?sid={session_id}", json={"choice": 0})
            assert response.status_code == 200
            
            answer_data = response.json()
            assert "correct" in answer_data
            assert "correct_answer" in answer_data
            assert isinstance(answer_data["correct"], bool)
    
    def test_session_isolation(self, test_db):
        """Test that different sessions are isolated"""
        # Start two different sessions
        response1 = client.post("/api/start?category=general")
        session1 = response1.json()["session_id"]
        
        response2 = client.post("/api/start?category=PSPO1")
        session2 = response2.json()["session_id"]
        
        assert session1 != session2  # Different session IDs
        
        # Verify both sessions work independently
        q1_response = client.get(f"/api/question?sid={session1}")
        q2_response = client.get(f"/api/question?sid={session2}")
        
        assert q1_response.status_code == 200
        assert q2_response.status_code == 200

class TestErrorHandling:
    """Test suite for error conditions"""
    
    def test_invalid_session_id(self):
        """Test handling of invalid session ID"""
        response = client.get("/api/question?sid=invalid-session-id")
        assert response.status_code == 400
        assert "Session not found" in response.json()["detail"]
    
    def test_missing_session_id(self):
        """Test handling of missing session ID"""
        response = client.get("/api/question")
        assert response.status_code == 400
        assert "No session id provided" in response.json()["detail"]
    
    def test_invalid_answer_format(self, test_db):
        """Test handling of invalid answer format"""
        # Start session and get question
        response = client.post("/api/start?category=general")
        session_id = response.json()["session_id"]
        
        # Submit invalid answer format
        response = client.post(f"/api/answer?sid={session_id}", json={"invalid": "format"})
        assert response.status_code == 422  # Validation error
    
    def test_start_without_category(self):
        """Test starting quiz without category defaults to general"""
        response = client.post("/api/start")
        assert response.status_code == 200
        
        data = response.json()
        # Should default to some category or general
        assert "session_id" in data

class TestDatabaseIntegrity:
    """Test suite for database integrity"""
    
    def test_question_counts_by_category(self, test_db):
        """Test that database has questions in each category"""
        # Count general questions (explanation IS NULL)
        general_count = test_db.execute(
            text("SELECT COUNT(*) FROM questions WHERE explanation IS NULL")
        ).scalar()
        
        # Count PSPO1 questions
        pspo1_count = test_db.execute(
            text("SELECT COUNT(*) FROM questions WHERE explanation = 'PSPO1'")
        ).scalar()
        
        # Count nursing questions
        nursing_count = test_db.execute(
            text("SELECT COUNT(*) FROM questions WHERE explanation = 'Verpleegkundig Rekenen'")
        ).scalar()
        
        assert general_count > 0, f"Expected general questions, found {general_count}"
        assert pspo1_count > 0, f"Expected PSPO1 questions, found {pspo1_count}"
        assert nursing_count > 0, f"Expected nursing questions, found {nursing_count}"
        
        print(f"Database integrity check: General={general_count}, PSPO1={pspo1_count}, Nursing={nursing_count}")
    
    def test_question_choices_exist(self, test_db):
        """Test that all questions have choices"""
        questions_without_choices = test_db.execute(
            text("""
                SELECT q.id, q.text 
                FROM questions q 
                LEFT JOIN choices c ON q.id = c.question_id 
                GROUP BY q.id, q.text 
                HAVING COUNT(c.id) = 0
                LIMIT 5
            """)
        ).fetchall()
        
        assert len(questions_without_choices) == 0, f"Found questions without choices: {questions_without_choices}"