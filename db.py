"""Database initialization and session management for Quiz App."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz.db")

engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=bool(os.getenv("SQL_ECHO"))
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class Base(DeclarativeBase):
    pass

def get_db():
    """FastAPI dependency to provide a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
