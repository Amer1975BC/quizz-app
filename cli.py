#!/usr/bin/env python3
from quiz_app import load_questions, Quiz
def main():
    questions = load_questions()
    quiz = Quiz(questions)
    print("Welkom bij de Quiz!\n")
    while quiz.has_next():
        q = quiz.next_question()
        print(q["question"])
        for i, c in enumerate(q["choices"]): print(f"  {i}. {c}")
        while True:
            try:
                ans = input("Jouw keuze (nummer): ")
                idx = int(ans.strip())
                if idx < 0 or idx >= len(q["choices"]): raise ValueError
                break
            except ValueError:
                print("Ongeldige keuze, probeer opnieuw.")
        correct = quiz.answer(q, idx)
        print("Correct!\n" if correct else f"Fout. Antwoord: {q['choices'][q['answer']]}\n")
    print(f"Klaar! Je score: {quiz.score}/{len(questions)}")
if __name__ == "__main__": main()
