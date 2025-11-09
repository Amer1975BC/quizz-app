from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from typing import Dict
from quiz_app import load_questions


app = FastAPI(title="Quiz App API")


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


def make_session():
    questions = load_questions()
    sid = str(uuid4())
    SESSIONS[sid] = {"questions": questions, "index": 0, "score": 0}
    return sid


def get_session(sid: str):
    s = SESSIONS.get(sid)
    if s is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return s


@app.post("/api/start")
def api_start(response: Response):
    """Start a new quiz session. Returns session id in cookie."""
    sid = make_session()
    # set cookie for client convenience
    response.set_cookie(key="quiz_session", value=sid, httponly=False)
    return {"session_id": sid}


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
    correct = q.get("answer")
    is_correct = (choice == correct)
    if is_correct:
        s["score"] += 1
    s["index"] += 1
    finished = s["index"] >= len(s["questions"])
    return {"correct": is_correct, "finished": finished, "score": s["score"], "total": len(s["questions"])}


@app.get("/api/result")
def api_result(sid: str = None, request: Request = None):
    if sid is None:
        sid = request.cookies.get("quiz_session")
    if not sid:
        raise HTTPException(status_code=400, detail="No session id provided")
    s = get_session(sid)
    return {"score": s["score"], "total": len(s["questions"])}


# Serve the static single-page frontend out of /static
app.mount("/", StaticFiles(directory="static", html=True), name="static")
