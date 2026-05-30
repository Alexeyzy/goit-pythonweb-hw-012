from datetime import date

from src.repository.contacts import create_contact, get_contacts
from src.repository.users import create_user, get_user_by_email
from src.schemas.contact import ContactCreate
from src.schemas.user import UserCreate


def test_create_user(db_session):
    user = create_user(UserCreate(username="Alex", email="alex@example.com", password="12345678"), db_session)
    assert user.id is not None
    assert user.password != "12345678"


def test_get_user_by_email(db_session):
    create_user(UserCreate(username="Alex", email="alex@example.com", password="12345678"), db_session)
    assert get_user_by_email("alex@example.com", db_session) is not None


def test_create_contact(db_session, user):
    contact = create_contact(ContactCreate(first_name="Ivan", last_name="Petrenko", email="ivan@example.com", phone="+380501112233", birthday=date.today()), db_session, user)
    assert contact.id is not None


def test_search_contacts(db_session, user):
    create_contact(ContactCreate(first_name="Ivan", last_name="Petrenko", email="ivan@example.com", phone="+380501112233", birthday=date.today()), db_session, user)
    assert len(get_contacts(db_session, user, search="Ivan")) == 1
