from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token
from app.models.user import User, UserRole
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def get_user_by_email_or_username(db: Session, email: str, username: str) -> User | None:
    return db.scalar(
        select(User).where(or_(User.email == email.lower(), User.username == username.lower()))
    )


def create_user(db: Session, payload: UserCreate, role: UserRole = UserRole.EMPLOYEE) -> User:
    user = User(
        email=payload.email.lower(),
        username=payload.username.lower(),
        full_name=payload.full_name.strip(),
        hashed_password=hash_password(payload.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def issue_tokens(user: User) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
