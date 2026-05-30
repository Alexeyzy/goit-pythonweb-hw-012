import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from src.conf.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True,
)


def upload_avatar(file: UploadFile, user_email: str) -> str:
    """Upload avatar to Cloudinary."""
    result = cloudinary.uploader.upload(file.file, public_id=f"contacts_api/{user_email}", overwrite=True)
    return result["secure_url"]
