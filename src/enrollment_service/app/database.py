from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Datenbank-URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mariadb+mariadbconnector://user:password@exams_db:3306/exams_db",
)

# Engine-Objekt, das die Verbindung zur Datenbank herstellt
# 'echo=True' bedeutet, dass alle SQL-Befehle im Terminal ausgegeben werden
engine = create_engine(
    DATABASE_URL, echo=True
)

# Session-Factory, die zum Erstellen neuer Datenbank-Sessions verwendet wird
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency-Funktion für das Abrufen einer Datenbank-Session
def get_db():
    """Datenbank-Abhängigkeit (Dependency)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
