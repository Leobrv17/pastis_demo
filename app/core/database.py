"""Database connection and initialization."""

import logging
from typing import List

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models.book import Book

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager."""

    client: AsyncIOMotorClient = None

    @classmethod
    async def connect(cls) -> None:
        """Connect to the database."""
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_url)
            await init_beanie(
                database=cls.client[settings.database_name],
                document_models=[Book]
            )
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def disconnect(cls) -> None:
        """Disconnect from the database."""
        if cls.client:
            cls.client.close()
            logger.info("Disconnected from MongoDB")

    @classmethod
    async def create_indexes(cls) -> None:
        """Create database indexes."""
        try:
            # Dans beanie 1.20.0, les indexes sont créés automatiquement
            # lors de l'initialisation avec init_beanie()
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Failed to create indexes: {e}")
            raise


# Database instance
db = Database()