from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """User creation schema."""

    username: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    username: str
    email: EmailStr
    confirmed: bool
    avatar: str | None = None
    role: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """JWT token response schema."""

    access_token: str
    token_type: str


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""

    token: str
    new_password: str = Field(min_length=6, max_length=100)
