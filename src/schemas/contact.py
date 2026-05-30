from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    """Base contact schema."""

    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=30)
    birthday: date
    additional_data: str | None = Field(default=None, max_length=500)


class ContactCreate(ContactBase):
    """Contact creation schema."""


class ContactUpdate(ContactBase):
    """Contact update schema."""


class ContactResponse(ContactBase):
    """Contact response schema."""

    id: int
    user_id: int

    model_config = {"from_attributes": True}
