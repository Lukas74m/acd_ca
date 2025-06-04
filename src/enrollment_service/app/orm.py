from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel
from datetime import date
from typing import List

Base = declarative_base()

class Exam(Base):
    __tablename__ = "Exam"

    pruefungs_id = Column(Integer, primary_key=True, autoincrement=True)
    prof_name   = Column(String(255), nullable=False)
    ects        = Column(Integer, nullable=False)
    datum       = Column(Date, nullable=False)
    modul       = Column(String(255), nullable=False)

    teilnehmer = relationship("TeilnehmerListe", back_populates="exam")


class ExamCreate(BaseModel):
    prof_name: str
    ects: int
    datum: date
    modul: str


class ExamResponse(BaseModel):
    pruefungs_id: int
    prof_name: str
    ects: int
    datum: date
    modul: str

    class Config:
        from_attributes = True


class TeilnehmerListe(Base):
    __tablename__ = "TeilnehmerListe"

    TeilnehmerListe_id = Column(Integer, primary_key=True, index=True)
    pruefungs_id       = Column(Integer, ForeignKey("Exam.pruefungs_id"), nullable=False)
    matrikelnummer     = Column(Integer, nullable=False)

    exam = relationship("Exam", back_populates="teilnehmer")

class NotenListe(Base):
    __tablename__ = "NotenListe"

    NotenListe_id = Column(Integer, primary_key=True, index=True)
    pruefungs_id = Column(Integer, nullable=False)
    note_id = Column(Integer, ForeignKey("Note.note_id"), nullable=False)

    #note = relationship("Note", back_populates="NotenListen")


class TeilnehmerListeCreate(BaseModel):
    pruefungs_id: int
    matrikelnummer: int


class TeilnehmerListeResponse(BaseModel):
    TeilnehmerListe_id: int
    pruefungs_id: int
    matrikelnummer: int

    class Config:
        from_attributes = True


class TeilnehmerListeWithExam(BaseModel):
    TeilnehmerListe_id: int
    pruefungs_id: int
    matrikelnummer: int
    exam: ExamResponse

    class Config:
        from_attributes = True

class NotenListeCreate(BaseModel):
    pruefungs_id: int
    note_id: int


class NotenListeResponse(BaseModel):
    NotenListe_id: int
    pruefungs_id: int
    note_id: int

    class Config:
        from_attributes = True


class NotenListeWithNote(BaseModel):
    NotenListe_id: int
    pruefungs_id: int
    note_id: int
    #note: NoteResponse

    class Config:
        from_attributes = True
