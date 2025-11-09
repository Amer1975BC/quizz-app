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
