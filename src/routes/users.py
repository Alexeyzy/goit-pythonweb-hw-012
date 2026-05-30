from fastapi import APIRouter, Depends, File, Request, UploadFile
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.entity.models import User
from src.repository import users as repository_users
from src.schemas.user import UserResponse
from src.services.auth import get_current_user, require_admin
from src.services.cloudinary_service import upload_avatar

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
def read_users_me(request: Request, current_user: User = Depends(get_current_user)):
    """Return current user."""
    return current_user


@router.patch("/avatar", response_model=UserResponse)
def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Update avatar. Only admin can use this endpoint."""
    avatar_url = upload_avatar(file, current_user.email)
    return repository_users.update_avatar(current_user.email, avatar_url, db)
