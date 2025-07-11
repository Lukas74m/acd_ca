from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from datetime import date

# Basis für Definition von SQLAlchemy Modellen
Base = declarative_base()


class Note(Base):
    __tablename__ = "Note"

    note_id = Column(Integer, primary_key=True, index=True)
    pruefungs_id = Column(Integer, nullable=False)
    datum = Column(Date, nullable=False)
    modul = Column(String(255), nullable=False)
    note = Column(String(5), nullable=False)


# Pydantic Modell für die Erstellung einer Note
class NoteCreate(BaseModel):
    pruefungs_id: int
    datum: date
    modul: str
    note: str


# Pydantic Modell für die Ausgabe einer Note
class NoteResponse(BaseModel):
    note_id: int
    pruefungs_id: int
    datum: date
    modul: str
    note: str

    class Config:
        from_attributes = True  # Mapping von ORM-Objekten
