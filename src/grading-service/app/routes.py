from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from orm import Note, NoteCreate, NoteResponse


def setup_routes(app):
    """Setup all API routes"""

    @app.get("/")
    async def root():
        return {"message": "Notes Microservice is running"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    @app.post("/notes/", response_model=NoteResponse)
    async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
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

    @app.get("/notes/", response_model=List[NoteResponse])
    async def get_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        notes = db.query(Note).offset(skip).limit(limit).all()
        return notes

    @app.get("/notes/{note_id}", response_model=NoteResponse)
    async def get_note(note_id: int, db: Session = Depends(get_db)):
        note = db.query(Note).filter(Note.id == note_id).first()
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return note

    @app.get("/notes/pruefung/{pruefungs_id}", response_model=List[NoteResponse])
    async def get_notes_by_pruefung(pruefungs_id: int, db: Session = Depends(get_db)):
        notes = db.query(Note).filter(Note.pruefungs_id == pruefungs_id).all()
        return notes

    @app.delete("/notes/{note_id}")
    async def delete_note(note_id: int, db: Session = Depends(get_db)):
        note = db.query(Note).filter(Note.id == note_id).first()
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        db.delete(note)
        db.commit()
        return {"message": "Note deleted successfully"}
