from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from datetime import date
from typing import List

Base = declarative_base()


class Exam(Base):
    __tablename__ = "Exam"

    pruefungs_id = Column(Integer, primary_key=True, autoincrement=True)
    prof_name = Column(String(255), nullable=False)
    ects = Column(Integer, nullable=False)
    datum = Column(Date, nullable=False)
    modul = Column(String(255), nullable=False)


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
