from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.conf.config import settings
from src.database.db import get_db
from src.repository import users as repository_users
from src.schemas.user import PasswordResetConfirm, PasswordResetRequest, Token, UserCreate, UserResponse
from src.services.auth import create_access_token, get_email_from_token, verify_password
from src.services.email import send_reset_password_email, send_verification_email
from src.services.auth import create_refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(body: UserCreate, db: Session = Depends(get_db)):
    """Register user."""
    user = repository_users.get_user_by_email(body.email, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    new_user = repository_users.create_user(body, db)
    send_verification_email(new_user.email)
    return new_user


@router.post("/login", response_model=Token)
def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user."""
    user = repository_users.get_user_by_email(body.username, db)
    if user is None or not verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    token = create_access_token({"sub": user.email}, timedelta(minutes=settings.access_token_expire_minutes))
    
    access_token = create_access_token(
    {"sub": user.email},
    timedelta(minutes=settings.access_token_expire_minutes),)
    refresh_token = create_refresh_token({"sub": user.email})
    return {"access_token": access_token,"refresh_token": refresh_token,"token_type": "bearer",}


@router.get("/confirmed_email/{token}")
def confirmed_email(token: str, db: Session = Depends(get_db)):
    """Confirm email."""
    email = get_email_from_token(token)
    user = repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post("/request_password_reset")
def request_password_reset(body: PasswordResetRequest, db: Session = Depends(get_db)):
    """Request password reset."""
    user = repository_users.get_user_by_email(body.email, db)
    if user:
        send_reset_password_email(user.email)
    return {"message": "If account exists, reset email was sent"}


@router.post("/reset_password")
def reset_password(body: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Reset password by token."""
    email = get_email_from_token(body.token)
    updated = repository_users.update_password(email, body.new_password, db)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "Password updated"}

@router.post("/refresh", response_model=Token)
def refresh_token(token: str):
    email = get_email_from_token(token)

    access_token = create_access_token(
        {"sub": email},
        timedelta(minutes=settings.access_token_expire_minutes),
    )
    new_refresh_token = create_refresh_token({"sub": email})

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
