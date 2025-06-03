from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from orm import Exam, ExamCreate, ExamResponse


def setup_routes(app):
    """Setup all API routes"""

    @app.get("/")
    async def root():
        return {"message": "Exams Microservice is running"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    @app.post("/exams/", response_model=ExamResponse)
    async def create_exam(exam: ExamCreate, db: Session = Depends(get_db)):
        db_exam = Exam(
            prof_name=exam.prof_name,
            ects=exam.ects,
            datum=exam.datum,
            modul=exam.modul,
        )
        db.add(db_exam)
        db.commit()
        db.refresh(db_exam)
        return db_exam

    @app.get("/exams/", response_model=List[ExamResponse])
    async def get_exams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        exams = db.query(Exam).offset(skip).limit(limit).all()
        return exams

    @app.get("/exams/{exam_id}", response_model=ExamResponse)
    async def get_exam(exam_id: int, db: Session = Depends(get_db)):
        exam = db.query(Exam).filter(Exam.pruefungs_id == exam_id).first()
        if exam is None:
            raise HTTPException(status_code=404, detail="Exam not found")
        return exam

    @app.get("/exams/modul/{modul_name}", response_model=List[ExamResponse])
    async def get_exams_by_modul(modul_name: str, db: Session = Depends(get_db)):
        exams = db.query(Exam).filter(Exam.modul == modul_name).all()
        return exams

    @app.delete("/exams/{exam_id}")
    async def delete_exam(exam_id: int, db: Session = Depends(get_db)):
        exam = db.query(Exam).filter(Exam.pruefungs_id == exam_id).first()
        if exam is None:
            raise HTTPException(status_code=404, detail="Exam not found")

        db.delete(exam)
        db.commit()
        return {"message": "Exam deleted successfully"}
