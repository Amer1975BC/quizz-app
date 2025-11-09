from sqlalchemy import Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import mapped_column, relationship
from db import Base

class Question(Base):
    __tablename__ = "questions"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    text = mapped_column(Text, nullable=False)
    explanation = mapped_column(Text, nullable=True)
    difficulty = mapped_column(Integer, default=1)
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")

class Choice(Base):
    __tablename__ = "choices"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id = mapped_column(ForeignKey("questions.id"), nullable=False)
    text = mapped_column(String(500), nullable=False)
    is_correct = mapped_column(Boolean, default=False)
    question = relationship("Question", back_populates="choices")
