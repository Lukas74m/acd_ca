from fastapi import HTTPException, Depends, Query, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import httpx
from orm import (
    Exam,
    TeilnehmerListe,
    ExamCreate,
    ExamResponse,
    TeilnehmerListeCreate,
    TeilnehmerListeResponse,
    TeilnehmerListeWithExam,
    NotenListe,
    NotenListeCreate,
    NotenListeResponse,
    NotenListeWithNote,
)

# from auth import (
#     User,
#     UserCreate,
#     UserResponse,
#     LoginRequest,
#     LoginResponse,
#     get_current_user,
#     require_professor,
#     require_student_or_professor,
#     authenticate_user,
#     create_user,
#     create_session_token,
#     logout_user,
#     check_student_access,
#     get_allowed_pruefungs_ids,
#     UserRole,
# )


async def get_note_from_grading_service(note_id: int, token: str) -> Optional[dict]:
    """Hole Note vom Grading-Service"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://grading-service:8001/Note/{note_id}",
                # headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching note: {e}")
            return None


def get_session_token(authorization: str = Header(None)):
    """Extrahiert Session-Token aus Authorization-Header"""
    if not authorization:
        return None
    if authorization.startswith("Bearer "):
        return authorization[7:]
    return authorization


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

    @app.post("/TeilnehmerListe/", response_model=TeilnehmerListeResponse)
    async def create_TeilnehmerListe_entry(
        entry: TeilnehmerListeCreate,
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        # current_user = get_current_user(token, db)
        # require_professor(current_user)

        db_entry = TeilnehmerListe(
            pruefungs_id=entry.pruefungs_id, matrikelnummer=entry.matrikelnummer
        )  # hier
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry

    @app.get("/TeilnehmerListe/", response_model=List[TeilnehmerListeWithExam])
    async def get_TeilnehmerListe(
        pruefungs_id: Optional[int] = Query(None),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        print("DEBUG TEST - TeilnehmerListe wurde aufgerufen")
        # current_user = get_current_user(token, db)
        # require_student_or_professor(current_user)

        query = db.query(TeilnehmerListe)

        # if current_user.role == UserRole.student:
        #     allowed_ids = get_allowed_pruefungs_ids(current_user)
        #     if not allowed_ids:
        #         return []
        #     query = query.filter(TeilnehmerListe.pruefungs_id.in_(allowed_ids))

        if pruefungs_id:
            # if current_user.role == UserRole.student:
            #     if not check_student_access(current_user, pruefungs_id):
            #         raise HTTPException(
            #             status_code=status.HTTP_403_FORBIDDEN,
            #             detail="Access denied for this exam",
            #         )
            query = query.filter(TeilnehmerListe.pruefungs_id == pruefungs_id)

        entries = query.offset(skip).limit(limit).all()
        print(f"Gefundene Teilnehmer-Einträge: {len(entries)}")
        result = []
        for entry in entries:
            exam = (
                db.query(Exam).filter(Exam.pruefungs_id == entry.pruefungs_id).first()
            )
            if not exam:
                print(f"Exam not found for pruefungs_id={entry.pruefungs_id}")
                raise HTTPException(404, detail="Exam not found")

            result.append(
                {
                    "TeilnehmerListe_id": entry.TeilnehmerListe_id,
                    "pruefungs_id": entry.pruefungs_id,
                    "matrikelnummer": entry.matrikelnummer,
                    "exam": exam,
                }
            )

        return result

    @app.post("/NotenListe/", response_model=NotenListeResponse)
    async def create_NotenListe_entry(
        entry: NotenListeCreate,
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        # note = note_db.query(Note).filter(Note.note_id == entry.note_id).first()
        # if not note:
        #    raise HTTPException(status_code=404, detail="Note not found")

        db_entry = NotenListe(pruefungs_id=entry.pruefungs_id, note_id=entry.note_id)
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry

    @app.get("/NotenListe/", response_model=List[NotenListeWithNote])
    async def get_NotenListe(
        pruefungs_id: Optional[int] = Query(None),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        query = db.query(NotenListe)
        if pruefungs_id:
            query = query.filter(NotenListe.pruefungs_id == pruefungs_id)

        entries = query.offset(skip).limit(limit).all()

        result = []
        for entry in entries:
            # Note vom anderen Service holen
            note_data = await get_note_from_grading_service(entry.note_id, token)
            result.append(
                {
                    "NotenListe_id": entry.NotenListe_id,
                    "pruefungs_id": entry.pruefungs_id,
                    "note_id": entry.note_id,
                    "note": note_data,
                }
            )

        return result

    # @app.delete("/NotenListe/{NotenListe_id}")
    # async def delete_NotenListe_entry(
    #     NotenListe_id: int,
    #     db: Session = Depends(get_db),
    #     token: str = Depends(get_session_token),
    # ):
    #     current_user = get_current_user(token, db)
    #     require_professor(current_user)

    #     entry = (
    #         db.query(NotenListe)
    #         .filter(NotenListe.NotenListe_id == NotenListe_id)
    #         .first()
    #     )
    #     if entry is None:
    #         raise HTTPException(status_code=404, detail="NotenListe entry not found")

    #     db.delete(entry)
    #     db.commit()
    #     return {"message": "NotenListe entry deleted successfully"}

    @app.put("/exams/{exam_id}", response_model=ExamResponse)
    async def update_exam(
        exam_id: int, exam_update: ExamCreate, db: Session = Depends(get_db)
    ):
        db_exam = db.query(Exam).filter(Exam.pruefungs_id == exam_id).first()
        if db_exam is None:
            raise HTTPException(status_code=404, detail="Exam not found")

        setattr(db_exam, "prof_name", exam_update.prof_name)
        setattr(db_exam, "ects", exam_update.ects)
        setattr(db_exam, "datum", exam_update.datum)
        setattr(db_exam, "modul", exam_update.modul)

        db.commit()
        db.refresh(db_exam)
        return db_exam
