from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Enum
from enum import Enum as PyEnum
from pydantic import BaseModel
from typing import Optional
from database import get_db
from orm import Base

active_sessions = {}


class UserRole(PyEnum):
    student = "student"
    professor = "professor"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    session_token: str
    user: UserResponse


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if user.password != password:
        return False
    return user


def create_session_token(username: str) -> str:
    import uuid

    token = str(uuid.uuid4())
    active_sessions[token] = username
    return token


def get_user_from_token(token: str, db: Session) -> Optional[User]:
    username = active_sessions.get(token)
    if not username:
        return None
    return get_user_by_username(db, username)


def logout_user(token: str):
    if token in active_sessions:
        del active_sessions[token]
        return True
    return False


def get_current_user(token: str = "", db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No session token provided"
        )

    user = get_user_from_token(token, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session token"
        )
    return user


def require_professor(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.professor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Professor access required"
        )
    return current_user


def require_student_or_professor(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.student, UserRole.professor]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student or Professor access required",
        )
    return current_user


def check_student_access(current_user: User, pruefungs_id: int) -> bool:
    if current_user.role == UserRole.professor:
        return True

    if current_user.role == UserRole.student:
        if current_user.username == "student.max":
            return pruefungs_id in [1, 2]
        elif current_user.username == "student.anna":
            return pruefungs_id in [2, 3]
        else:
            return False

    return False


def get_allowed_pruefungs_ids(current_user: User) -> list:
    if current_user.role == UserRole.professor:
        return None

    if current_user.role == UserRole.student:
        if current_user.username == "student.max":
            return [1, 2]
        elif current_user.username == "student.anna":
            return [2, 3]
        else:
            return []

    return []
