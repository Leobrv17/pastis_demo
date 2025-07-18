"""Configuration settings for the library API."""

import os
from typing import Optional

from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""

    # Database
    mongodb_url: str = os.getenv(
        "MONGODB_URL",
        "mongodb://admin:password@localhost:27017/library?authSource=admin"
    )
    database_name: str = os.getenv("DATABASE_NAME", "library")

    # API
    api_title: str = "Library API"
    api_description: str = "API de gestion de bibliothèque"
    api_version: str = "1.0.0"

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Pagination
    default_page_size: int = 10
    max_page_size: int = 100


settings = Settings()