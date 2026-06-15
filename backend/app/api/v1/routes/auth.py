from collections import defaultdict
from time import monotonic
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import get_db
from app.models.audit_log import AuditAction
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import (
    authenticate_user,
    create_user,
    get_user_by_email_or_username,
    issue_tokens,
)
from app.services.audit_service import record_audit_log

router = APIRouter(prefix="/auth")
login_attempts: dict[str, list[float]] = defaultdict(list)


def enforce_login_rate_limit(request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    now = monotonic()
    window_start = now - 60
    login_attempts[client_ip] = [attempt for attempt in login_attempts[client_ip] if attempt > window_start]

    if len(login_attempts[client_ip]) >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again in one minute.",
        )

    login_attempts[client_ip].append(now)


def validate_password_strength(password: str) -> None:
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(not char.isalnum() for char in password)

    if not all([has_upper, has_lower, has_digit, has_symbol]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must include uppercase, lowercase, number, and symbol characters.",
        )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Annotated[Session, Depends(get_db)]) -> User:
    validate_password_strength(payload.password)

    existing_user = get_user_by_email_or_username(db, payload.email, payload.username)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username is already registered.",
        )

    user_count = db.query(User).count()
    role = UserRole.ADMIN if user_count == 0 else UserRole.EMPLOYEE
    user = create_user(db, payload, role=role)
    record_audit_log(
        db,
        action=AuditAction.USER_REGISTER,
        entity_type="user",
        entity_id=str(user.id),
        actor=user,
        description=f"{user.full_name} registered as {user.role}",
    )
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    enforce_login_rate_limit(request)
    user = authenticate_user(db, payload.email, payload.password)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    record_audit_log(
        db,
        action=AuditAction.USER_LOGIN,
        entity_type="user",
        entity_id=str(user.id),
        actor=user,
        description=f"{user.full_name} logged in",
    )
    return issue_tokens(user)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
