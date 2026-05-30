from src.conf.config import settings
from src.services.auth import create_email_token, create_reset_password_token


def send_verification_email(email: str) -> None:
    """Print email verification link to console."""
    token = create_email_token(email)
    print(f"Verification email for {email}: {settings.base_url}/api/auth/confirmed_email/{token}")


def send_reset_password_email(email: str) -> None:
    """Print password reset link to console."""
    token = create_reset_password_token(email)
    print(f"Reset password email for {email}: {settings.base_url}/api/auth/reset_password/{token}")
