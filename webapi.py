import os
from fastapi import FastAPI, HTTPException, Request, Response, Depends, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from uuid import uuid4
from typing import Dict
from typing import List, Dict
from sqlalchemy import func
from sqlalchemy.orm import selectinload, Session
from db import Base, engine, SessionLocal
from models import Question, Choice
from pydantic import BaseModel



app = FastAPI(title="Quiz App API")

# Basic Auth setup for /admin
security = HTTPBasic()
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
# Password file for runtime updates
ADMIN_PASS_FILE = os.environ.get("ADMIN_PASS_FILE", "/app/admin_pass.txt")
def get_admin_pass():
    try:
        with open(ADMIN_PASS_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return os.environ.get("ADMIN_PASS", "admin")
def set_admin_pass(new_pass: str):
    with open(ADMIN_PASS_FILE, "w") as f:
        f.write(new_pass.strip())

# Ensure tables exist (idempotent)
Base.metadata.create_all(engine)


# Allow same-origin requests (static files served from same host). Adjust if serving frontend separately.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory session store: session_id -> {questions, index, score}
SESSIONS: Dict[str, Dict] = {}


# Load questions from the database and adapt to current questionnaire format
def load_questions_from_db(category=None) -> List[Dict]:
    db = SessionLocal()
    try:
        # Filter by category with strict separation
        query = db.query(Question).options(selectinload(Question.choices))
        
        if category == 'PSPO1':
            # Only PSPO1 questions
            query = query.filter(Question.explanation == 'PSPO1')
        elif category == 'Verpleegkundig Rekenen':
            # Only nursing questions
            query = query.filter(Question.explanation == 'Verpleegkundig Rekenen')
        else:
            # General quiz: only questions without specific category (explanation IS NULL)
            query = query.filter(Question.explanation.is_(None))
        
        # Get questions in random order using SQLAlchemy func.random()
        qs = query.order_by(func.random()).all()
        out = []
        for q in qs:
            choices = [c.text for c in q.choices]
            # Handle multiple correct answers
            correct_indices = [i for i, c in enumerate(q.choices) if c.is_correct]
            # For backward compatibility, use first correct answer as "answer"
            ans_idx = correct_indices[0] if correct_indices else None
            out.append({"text": q.text, "choices": choices, "answer": ans_idx, "correct_answers": correct_indices})
        return out
    finally:
        db.close()


def make_session(category=None):
    # Prefer DB questions; if empty, keep compatibility with JSON fallback
    questions = load_questions_from_db(category)
    if not questions:
        from quiz_app import load_questions as _json_loader
        questions = _json_loader()
    sid = str(uuid4())
    SESSIONS[sid] = {"questions": questions, "index": 0, "score": 0, "category": category}
    return sid


def get_session(sid: str):
    s = SESSIONS.get(sid)
    if s is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return s

# --- DB dependency (wrap SessionLocal) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic schemas for admin CRUD ---
class QuestionCreate(BaseModel):
    text: str
    choices: List[str]
    correct_index: int

class QuestionUpdate(BaseModel):
    text: str | None = None
    choices: List[str] | None = None
    correct_index: int | None = None

# --- Serializer helper ---
def serialize_question(q: Question) -> Dict:
    return {
        "id": q.id,
        "text": q.text,
        "choices": [
            {"id": c.id, "text": c.text, "is_correct": c.is_correct}
            for c in q.choices
        ],
    }


@app.post("/api/start")
def api_start(response: Response, category: str = Query(None)):
    """Start a new quiz session with optional category. Returns session id in cookie."""
    sid = make_session(category)
    # set cookie for client convenience
    response.set_cookie(key="quiz_session", value=sid, httponly=False)
    return {"session_id": sid, "category": category}


@app.get("/api/question")
def api_question(sid: str = None, request: Request = None):
    """Return the next question for the session. Provide sid as query param or cookie 'quiz_session'."""
    if sid is None:
        sid = request.cookies.get("quiz_session")
    if not sid:
        raise HTTPException(status_code=400, detail="No session id provided")
    s = get_session(sid)
    idx = s["index"]
    if idx >= len(s["questions"]):
        return {"finished": True}
    q = s["questions"][idx].copy()
    # remove the answer from the payload
    q.pop("answer", None)
    return {"finished": False, "question": q, "index": idx, "total": len(s["questions"])}


@app.post("/api/answer")
@app.post("/api/answer")
def api_answer(payload: Dict, sid: str = None, request: Request = None):
    """Submit an answer: payload must contain {'choice': int}."""
    if sid is None:
        sid = request.cookies.get("quiz_session")
    if not sid:
        raise HTTPException(status_code=400, detail="No session id provided")
    s = get_session(sid)
    idx = s["index"]
    if idx >= len(s["questions"]):
        return {"finished": True}
    try:
        choice = int(payload.get("choice"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid choice")
    q = s["questions"][idx]
    # Support both single and multiple correct answers
    correct_answers = q.get("correct_answers", [])
    if not correct_answers and q.get("answer") is not None:
        correct_answers = [q.get("answer")]
    is_correct = choice in correct_answers
    if is_correct:
        s["score"] += 1
    s["index"] += 1
    finished = s["index"] >= len(s["questions"])
    return {"correct": is_correct, "finished": finished, "score": s["score"], "total": len(s["questions"]), "correct_answers": correct_answers}


@app.get("/api/result")
def api_result(sid: str = None, request: Request = None):
    if sid is None:
        sid = request.cookies.get("quiz_session")
    if not sid:
        raise HTTPException(status_code=400, detail="No session id provided")
    s = get_session(sid)
    return {"score": s["score"], "total": len(s["questions"])}

# ---------------- Admin CRUD Endpoints -----------------
@app.get("/api/admin/questions")
def admin_list_questions(db: Session = Depends(get_db)):
    qs = db.query(Question).options(selectinload(Question.choices)).all()
    return [serialize_question(q) for q in qs]

@app.post("/api/admin/questions")
def admin_create_question(payload: QuestionCreate, db: Session = Depends(get_db)):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Question text is required")
    if payload.choices is None or len(payload.choices) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 choices")
    if payload.correct_index < 0 or payload.correct_index >= len(payload.choices):
        raise HTTPException(status_code=400, detail="correct_index out of range")

    q = Question(text=payload.text.strip())
    db.add(q)
    db.flush()  # assign id
    for i, txt in enumerate(payload.choices):
        db.add(Choice(text=txt, is_correct=(i == payload.correct_index), question_id=q.id))
    db.commit()
    db.refresh(q)
    _ = q.choices  # ensure loaded
    return serialize_question(q)

@app.patch("/api/admin/questions/{qid}")
def admin_update_question(qid: int, payload: QuestionUpdate, db: Session = Depends(get_db)):
    q = db.query(Question).options(selectinload(Question.choices)).filter(Question.id == qid).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    if payload.text is not None:
        if not payload.text.strip():
            raise HTTPException(status_code=400, detail="Question text cannot be empty")
        q.text = payload.text.strip()

    if payload.choices is not None:
        if len(payload.choices) < 2:
            raise HTTPException(status_code=400, detail="Provide at least 2 choices")
        if payload.correct_index is None:
            raise HTTPException(status_code=400, detail="Provide correct_index when replacing choices")
        if payload.correct_index < 0 or payload.correct_index >= len(payload.choices):
            raise HTTPException(status_code=400, detail="correct_index out of range")
        # replace whole choice set
        for c in list(q.choices):
            db.delete(c)
        db.flush()
        for i, txt in enumerate(payload.choices):
            db.add(Choice(text=txt, is_correct=(i == payload.correct_index), question_id=q.id))
    elif payload.correct_index is not None:
        if payload.correct_index < 0 or payload.correct_index >= len(q.choices):
            raise HTTPException(status_code=400, detail="correct_index out of range")
        for i, c in enumerate(q.choices):
            c.is_correct = (i == payload.correct_index)

    db.commit()
    db.refresh(q)
    _ = q.choices
    return serialize_question(q)

@app.delete("/api/admin/questions/{qid}", status_code=204)
def admin_delete_question(qid: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == qid).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(q)
    db.commit()
    return Response(status_code=204)


# Serve static assets under /static, and index with no-cache at root
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/static/{rest_of_path:path}")
async def serve_static_nocache(rest_of_path: str):
    """Override to add no-cache headers for static JS/CSS."""
    from pathlib import Path
    file_path = Path("static") / rest_of_path
    if not file_path.exists():
        raise HTTPException(404, "File not found")
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    # Force correct Content-Type for .js files
    if rest_of_path.endswith('.js'):
        return FileResponse(file_path, headers=headers, media_type="application/javascript")
    return FileResponse(file_path, headers=headers)

@app.get("/")
def serve_index():
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
    return FileResponse("static/index.html", headers=headers)

@app.get("/admin")
def serve_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_pass = secrets.compare_digest(credentials.password, get_admin_pass())
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0", "Pragma": "no-cache"}
    return FileResponse("static/admin.html", headers=headers)
# --- Admin password change endpoint ---
from pydantic import BaseModel
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

@app.post("/api/admin/password")
def change_admin_password(payload: PasswordChangeRequest, credentials: HTTPBasicCredentials = Depends(security)):
    # Only allow if current password matches
    correct_user = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_pass = secrets.compare_digest(credentials.password, get_admin_pass())
    if not (correct_user and correct_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized", headers={"WWW-Authenticate": "Basic"})
    # Validate current password
    if not secrets.compare_digest(payload.current_password, get_admin_pass()):
        raise HTTPException(status_code=403, detail="Current password incorrect")
    # Validate new password
    if not payload.new_password or len(payload.new_password) < 4:
        raise HTTPException(status_code=400, detail="New password too short")
    set_admin_pass(payload.new_password)
    return {"success": True}

