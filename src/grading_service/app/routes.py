from fastapi import HTTPException, Depends, Query, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from orm import (
    Note,
    NoteCreate,
    NoteResponse,
)
from auth import (
    UserCreate,
    UserResponse,
    LoginRequest,
    LoginResponse,
    get_current_user,
    require_professor,
    require_student_or_professor,
    authenticate_user,
    create_user,
    create_session_token,
    logout_user,
    check_student_access,
    get_allowed_pruefungs_ids,
    UserRole,
)


def get_session_token(authorization: str = Header(None)):
    """Extrahiert Session-Token aus Authorization-Header"""
    if not authorization:
        return None
    if authorization.startswith("Bearer "):
        return authorization[7:]
    return authorization


def setup_routes(app):
    """Setup all API routes for Note-Microservice with Authentication"""

    @app.get("/")
    async def root():
        return {"message": "Note-Microservice is running"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    @app.post("/register", response_model=UserResponse)
    async def register_user(user: UserCreate, db: Session = Depends(get_db)):
        """Neuen Benutzer registrieren"""
        return create_user(db, user)

    @app.post("/login", response_model=LoginResponse)
    async def login_for_access_token(
        login_data: LoginRequest, db: Session = Depends(get_db)
    ):
        """Benutzer anmelden und Session-Token erhalten"""
        user = authenticate_user(db, login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        session_token = create_session_token(user.username)
        return LoginResponse(
            session_token=session_token,
            user=UserResponse(
                user_id=user.user_id,
                username=user.username,
                email=user.email,
                role=user.role,
            ),
        )

    @app.get("/me", response_model=UserResponse)
    async def read_users_me(
        token: str = Depends(get_session_token), db: Session = Depends(get_db)
    ):
        """Aktuelle Benutzerinformationen abrufen"""
        current_user = get_current_user(token, db)
        return current_user

    @app.post("/logout")
    async def logout(token: str = Depends(get_session_token)):
        if token:
            success = logout_user(token)
            if success:
                return {"message": "Successfully logged out"}
            else:
                return {"message": "Token not found, already logged out"}
        return {"message": "No token provided"}

    @app.post("/Note/", response_model=NoteResponse)
    async def create_note(
        note: NoteCreate,
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        current_user = get_current_user(token, db)
        require_professor(current_user)

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

    @app.get("/Note/", response_model=List[NoteResponse])
    async def get_Note(
        skip: int = 0,
        limit: int = 100,
        pruefungs_id: Optional[int] = Query(None),
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        current_user = get_current_user(token, db)
        require_student_or_professor(current_user)

        query = db.query(Note)

        if current_user.role == UserRole.student:
            allowed_ids = get_allowed_pruefungs_ids(current_user)
            if not allowed_ids:
                return []
            query = query.filter(Note.pruefungs_id.in_(allowed_ids))

        if pruefungs_id:
            if current_user.role == UserRole.student:
                if not check_student_access(current_user, pruefungs_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied for this exam",
                    )
            query = query.filter(Note.pruefungs_id == pruefungs_id)

        notes = query.offset(skip).limit(limit).all()
        return notes

    @app.get("/Note/{note_id}", response_model=NoteResponse)
    async def get_note(
        note_id: int,
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        current_user = get_current_user(token, db)
        require_student_or_professor(current_user)

        note = db.query(Note).filter(Note.note_id == note_id).first()
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        if not check_student_access(current_user, note.pruefungs_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied for this note",
            )

        return note

    @app.put("/Note/{note_id}", response_model=NoteResponse)
    async def update_note(
        note_id: int,
        note_update: NoteCreate,
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        current_user = get_current_user(token, db)
        require_professor(current_user)

        db_note = db.query(Note).filter(Note.note_id == note_id).first()
        if db_note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        db_note.pruefungs_id = note_update.pruefungs_id
        db_note.datum = note_update.datum
        db_note.modul = note_update.modul
        db_note.note = note_update.note

        db.commit()
        db.refresh(db_note)
        return db_note

    @app.delete("/Note/{note_id}")
    async def delete_note(
        note_id: int,
        db: Session = Depends(get_db),
        token: str = Depends(get_session_token),
    ):
        current_user = get_current_user(token, db)
        require_professor(current_user)

        note = db.query(Note).filter(Note.note_id == note_id).first()
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")

        db.delete(note)
        db.commit()
        return {"message": "Note deleted successfully"}
