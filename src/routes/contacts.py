from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.entity.models import User
from src.repository import contacts as repository_contacts
from src.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from src.services.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
def get_contacts(skip: int = 0, limit: int = Query(default=100, le=500), search: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Return contacts."""
    return repository_contacts.get_contacts(db, current_user, skip, limit, search)


@router.get("/birthdays", response_model=list[ContactResponse])
def get_birthdays(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Return upcoming birthdays."""
    return repository_contacts.get_upcoming_birthdays(db, current_user)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Return one contact."""
    contact = repository_contacts.get_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(body: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create contact."""
    return repository_contacts.create_contact(body, db, current_user)


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, body: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update contact."""
    contact = repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete contact."""
    contact = repository_contacts.remove_contact(contact_id, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
