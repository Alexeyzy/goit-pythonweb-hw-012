from sqlalchemy.orm import Session

from src.entity.models import User
from src.schemas.user import UserCreate
from src.services.cache import delete_cache


def get_user_by_email(email: str, db: Session) -> User | None:
    """Find user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(body: UserCreate, db: Session) -> User:
    """Create user with hashed password."""
    from src.services.auth import get_password_hash

    user = User(username=body.username, email=body.email, password=get_password_hash(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def confirmed_email(email: str, db: Session) -> None:
    """Mark email as confirmed."""
    user = get_user_by_email(email, db)
    if user:
        user.confirmed = True
        db.commit()
        delete_cache(f"user:{email}")


def update_avatar(email: str, avatar_url: str, db: Session) -> User | None:
    """Update avatar URL."""
    user = get_user_by_email(email, db)
    if user:
        user.avatar = avatar_url
        db.commit()
        db.refresh(user)
        delete_cache(f"user:{email}")
    return user


def update_password(email: str, password: str, db: Session) -> bool:
    """Update user password."""
    from src.services.auth import get_password_hash

    user = get_user_by_email(email, db)
    if not user:
        return False
    user.password = get_password_hash(password)
    db.commit()
    delete_cache(f"user:{email}")
    return True
