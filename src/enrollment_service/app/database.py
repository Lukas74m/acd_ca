from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mariadb+mariadbconnector://user:password@exams_db:3306/exams_db",
)

engine = create_engine(
    DATABASE_URL, echo=True
)  # echo=True for debugging/verbose output

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()