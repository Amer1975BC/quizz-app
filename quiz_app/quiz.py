import json
import os
from typing import List, Dict, Any


def load_questions(path: str = None) -> List[Dict[str, Any]]:
    """Load questions from a JSON file. If path is None, load bundled questions."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "questions.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class Quiz:
    def __init__(self, questions: List[Dict[str, Any]]):
        self.questions = questions
        self.index = 0
        self.score = 0

    def has_next(self) -> bool:
        return self.index < len(self.questions)

    def next_question(self) -> Dict[str, Any]:
        if not self.has_next():
            raise IndexError("No more questions")
        q = self.questions[self.index]
        self.index += 1
        return q

    def answer(self, question: Dict[str, Any], choice_index: int) -> bool:
        """Submit an answer for a question. Returns True if correct."""
        correct = question.get("answer")
        is_correct = (choice_index == correct)
        if is_correct:
            self.score += 1
        return is_correct
