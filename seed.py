from db import Base, engine, SessionLocal
from models import Question, Choice

Base.metadata.create_all(engine)

def ensure_seed():
    s = SessionLocal()
    try:
        if s.query(Question).count() == 0:
            q1 = Question(text='Wat is 2 + 2?', difficulty=1)
            q1.choices = [Choice(text='3', is_correct=False), Choice(text='4', is_correct=True), Choice(text='5', is_correct=False)]
            q2 = Question(text='Welke kleur heeft de lucht op een heldere dag?', difficulty=1)
            q2.choices = [Choice(text='Blauw', is_correct=True), Choice(text='Groen', is_correct=False), Choice(text='Rood', is_correct=False)]
            s.add_all([q1, q2])
            s.commit()
            print('Seeded initial questions (2).')
        else:
            print('Questions already present, skipping seed.')
    finally:
        s.close()

if __name__ == '__main__':
    ensure_seed()
