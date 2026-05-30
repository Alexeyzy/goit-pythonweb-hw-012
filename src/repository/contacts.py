from datetime import date, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.entity.models import Contact, User
from src.schemas.contact import ContactCreate, ContactUpdate


def get_contacts(db: Session, user: User, skip: int = 0, limit: int = 100, search: str | None = None) -> list[Contact]:
    """Return user's contacts with optional search."""
    query = db.query(Contact).filter(Contact.user_id == user.id)
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Contact.first_name.ilike(pattern), Contact.last_name.ilike(pattern), Contact.email.ilike(pattern)))
    return query.offset(skip).limit(limit).all()


def get_contact(contact_id: int, db: Session, user: User) -> Contact | None:
    """Return one user's contact."""
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()


def create_contact(body: ContactCreate, db: Session, user: User) -> Contact:
    """Create user's contact."""
    contact = Contact(**body.model_dump(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update_contact(contact_id: int, body: ContactUpdate, db: Session, user: User) -> Contact | None:
    """Update user's contact."""
    contact = get_contact(contact_id, db, user)
    if contact is None:
        return None
    for key, value in body.model_dump().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


def remove_contact(contact_id: int, db: Session, user: User) -> Contact | None:
    """Delete user's contact."""
    contact = get_contact(contact_id, db, user)
    if contact is None:
        return None
    db.delete(contact)
    db.commit()
    return contact


def get_upcoming_birthdays(db: Session, user: User) -> list[Contact]:
    """Return contacts with birthdays in next seven days."""
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    result = []
    for contact in contacts:
        birthday = contact.birthday.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        if today <= birthday <= end_date:
            result.append(contact)
    return result
