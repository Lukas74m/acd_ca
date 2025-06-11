from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel
from datetime import date
from typing import Optional

# Basis für ORM-Modelle
Base = declarative_base()

# Prüfungen Objekt
class Exam(Base):
    __tablename__ = "Exam"

    pruefungs_id = Column(Integer, primary_key=True, autoincrement=True) 
    prof_name   = Column(String(255), nullable=False) 
    ects        = Column(Integer, nullable=False)    
    datum       = Column(Date, nullable=False)        
    modul       = Column(String(255), nullable=False)

    teilnehmer = relationship("TeilnehmerListe", back_populates="exam")


# Prüfungen erstellen
class ExamCreate(BaseModel):
    prof_name: str
    ects: int
    datum: date
    modul: str


# Prüfungen Ausgabe
class ExamResponse(BaseModel):
    pruefungs_id: int
    prof_name: str
    ects: int
    datum: date
    modul: str

    class Config:
        from_attributes = True


# Teilnehmerliste
class TeilnehmerListe(Base):
    __tablename__ = "TeilnehmerListe"

    TeilnehmerListe_id = Column(Integer, primary_key=True, index=True)
    pruefungs_id       = Column(Integer, ForeignKey("Exam.pruefungs_id"), nullable=False)  # Referenz zur Prüfung
    matrikelnummer     = Column(Integer, nullable=False)  # Studierenden-ID

    exam = relationship("Exam", back_populates="teilnehmer")  # Beziehung zur Prüfung


# Notenliste
class NotenListe(Base):
    __tablename__ = "NotenListe"

    NotenListe_id = Column(Integer, primary_key=True, index=True)
    pruefungs_id = Column(Integer, nullable=False) 
    note_id = Column(Integer, nullable=False)       


# Teilnehmerliste erstellen
class TeilnehmerListeCreate(BaseModel):
    pruefungs_id: int
    matrikelnummer: int


# Teilnehmerliste Ausgabe
class TeilnehmerListeResponse(BaseModel):
    TeilnehmerListe_id: int
    pruefungs_id: int
    matrikelnummer: int

    class Config:
        from_attributes = True


# Teilnehmerliste und Prüfungen
class TeilnehmerListeWithExam(BaseModel):
    TeilnehmerListe_id: int
    pruefungs_id: int
    matrikelnummer: int
    exam: ExamResponse 

    class Config:
        from_attributes = True


# Note erstellen
class NotenListeCreate(BaseModel):
    pruefungs_id: int
    note_id: int


# Note Ausgabe
class NotenListeResponse(BaseModel):
    NotenListe_id: int
    pruefungs_id: int
    note_id: int

    class Config:
        from_attributes = True


# Notenliste mit Note
class NotenListeWithNote(BaseModel):
    NotenListe_id: int
    pruefungs_id: int
    note_id: int
    note: Optional[dict] = None 

    class Config:
        from_attributes = True
