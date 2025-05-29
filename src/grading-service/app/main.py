from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import date

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mariadb+mariadbconnector://user:password@localhost:3306/microservice_db",
)

Base = declarative_base()


class Note(Base):
    __tablename__ = "Note"

    id = Column(Integer, primary_key=True, index=True)
    pruefungs_id = Column(Integer, nullable=False)
    datum = Column(Date, nullable=False)
    modul = Column(String(255), nullable=False)
    note = Column(String(5), nullable=False)


class NoteCreate(BaseModel):
    pruefungs_id: int
    datum: date
    modul: str
    note: str


class NoteResponse(BaseModel):
    id: int
    pruefungs_id: int
    datum: date
    modul: str
    note: str

    class Config:
        from_attributes = True


class MicroService:
    def __init__(self):
        self.app = FastAPI(title="Notes Microservice", version="1.0.0")
        self.engine = create_engine(DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        Base.metadata.create_all(bind=self.engine, checkfirst=True)

        self._setup_routes()

    def get_db(self):
        """Database dependency"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def _setup_routes(self):
        """Setup API routes"""

        @self.app.get("/")
        async def root():
            return {"message": "Notes Microservice is running"}

        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy"}

        @self.app.post("/notes/", response_model=NoteResponse)
        async def create_note(note: NoteCreate, db: Session = Depends(self.get_db)):
            db_note = Note(
                pruefungs_id=note.pruefungs_id,
                datum=note.datum,
                modul=note.modul,
                note=note.note,
            )
            db.add(db_note)
            db.commit()
            db.refresh(db_note)
            return db_note

        @self.app.get("/notes/", response_model=List[NoteResponse])
        async def get_notes(
            skip: int = 0, limit: int = 100, db: Session = Depends(self.get_db)
        ):
            notes = db.query(Note).offset(skip).limit(limit).all()
            return notes

        @self.app.get("/notes/{note_id}", response_model=NoteResponse)
        async def get_note(note_id: int, db: Session = Depends(self.get_db)):
            note = db.query(Note).filter(Note.id == note_id).first()
            if note is None:
                raise HTTPException(status_code=404, detail="Note not found")
            return note

        @self.app.get(
            "/notes/pruefung/{pruefungs_id}", response_model=List[NoteResponse]
        )
        async def get_notes_by_pruefung(
            pruefungs_id: int, db: Session = Depends(self.get_db)
        ):
            notes = db.query(Note).filter(Note.pruefungs_id == pruefungs_id).all()
            return notes

        @self.app.delete("/notes/{note_id}")
        async def delete_note(note_id: int, db: Session = Depends(self.get_db)):
            note = db.query(Note).filter(Note.id == note_id).first()
            if note is None:
                raise HTTPException(status_code=404, detail="Note not found")

            db.delete(note)
            db.commit()
            return {"message": "Note deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    service = MicroService()
    uvicorn.run(service.app, host="localhost", port=8000)
