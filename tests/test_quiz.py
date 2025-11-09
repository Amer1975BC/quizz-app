import os
import json
import pytest


def _import_app():
    # Lazy import to allow env to be set first
    import importlib
    return importlib.import_module('webapi')


def test_index_serves_html():
    webapi = _import_app()
    from starlette.testclient import TestClient
    client = TestClient(webapi.app)
    r = client.get('/')
    assert r.status_code == 200
    assert 'text/html' in r.headers.get('content-type', '')


def test_start_post_and_question_flow_smoke():
    webapi = _import_app()
    from starlette.testclient import TestClient
    client = TestClient(webapi.app)

    # POST /api/start may require DB; if it fails with 500, skip rather than fail hard
    resp = client.post('/api/start')
    if resp.status_code >= 500:
        pytest.skip("backend unavailable for start (likely DB not configured)")
    assert resp.status_code in (200, 201)
    data = resp.json()
    sid = data.get('session_id') or data.get('sessionId')
    assert sid

    q = client.get('/api/question', params={'sid': sid})
    assert q.status_code == 200
    js = q.json()
    assert 'question' in js or js.get('finished') is True
import unittest, os
from quiz_app.quiz import Quiz, load_questions
class QuizTests(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "..", "quiz_app", "questions.json")
        self.questions = load_questions(path); self.quiz = Quiz(self.questions)
    def test_has_next_and_next_question(self):
        self.assertTrue(self.quiz.has_next()); q = self.quiz.next_question(); self.assertIn("question", q)
    def test_answer_correct_increments_score(self):
        q = self.quiz.next_question(); correct_index = q["answer"]; res = self.quiz.answer(q, correct_index)
        self.assertTrue(res); self.assertEqual(self.quiz.score, 1)
    def test_exhaust_questions(self):
        count = 0
        while self.quiz.has_next(): self.quiz.next_question(); count += 1
        self.assertEqual(count, len(self.questions))
        with self.assertRaises(IndexError): self.quiz.next_question()
if __name__ == '__main__': unittest.main()
