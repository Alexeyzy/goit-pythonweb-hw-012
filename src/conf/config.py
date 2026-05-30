from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env."""

    database_url: str
    redis_host: str = "redis"
    redis_port: int = 6379
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    base_url: str
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
