from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

Base = declarative_base()


class Note(Base):
    __tablename__ = "Note"

    note_id = Column(Integer, primary_key=True, index=True)
    pruefungs_id = Column(Integer, nullable=False)
    datum = Column(Date, nullable=False)
    modul = Column(String(255), nullable=False)
    note = Column(String(5), nullable=False)

    Notelisten = relationship("Noteliste", back_populates="note")


class Noteliste(Base):
    __tablename__ = "Noteliste"

    Noteliste_id = Column(Integer, primary_key=True, index=True)
    pruefungs_id = Column(Integer, nullable=False)
    note_id = Column(Integer, ForeignKey("Note.note_id"), nullable=False)

    note = relationship("Note", back_populates="Notelisten")


class NoteCreate(BaseModel):
    pruefungs_id: int
    datum: date
    modul: str
    note: str


class NoteResponse(BaseModel):
    note_id: int
    pruefungs_id: int
    datum: date
    modul: str
    note: str

    class Config:
        from_attributes = True


class NotelisteCreate(BaseModel):
    pruefungs_id: int
    note_id: int


class NotelisteResponse(BaseModel):
    Noteliste_id: int
    pruefungs_id: int
    note_id: int

    class Config:
        from_attributes = True


class NotelisteWithNote(BaseModel):
    Noteliste_id: int
    pruefungs_id: int
    note_id: int
    note: NoteResponse

    class Config:
        from_attributes = True
