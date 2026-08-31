"""MongoDB connection and management."""

import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    """MongoDB connection manager."""

    _instance: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect(cls) -> AsyncIOMotorDatabase:
        """Connect to MongoDB."""
        if cls._instance is None:
            logger.info(f"Connecting to MongoDB at {settings.MONGO_URI}")
            cls._instance = AsyncIOMotorClient(settings.MONGO_URI)
            cls._db = cls._instance[settings.DATABASE_NAME]

            # Verify connection
            await cls._instance.admin.command("ping")
            logger.info("MongoDB connection successful")

            # Create indexes
            await cls._create_indexes()

        return cls._db

    @classmethod
    async def disconnect(cls) -> None:
        """Disconnect from MongoDB."""
        if cls._instance is not None:
            logger.info("Disconnecting from MongoDB")
            cls._instance.close()
            cls._instance = None
            cls._db = None

    @classmethod
    async def _create_indexes(cls) -> None:
        """Create database indexes."""
        if cls._db is None:
            return

        logger.info("Creating database indexes")

        # Books collection indexes
        books = cls._db["books"]

        # Unique index on id (application-level ID)
        await books.create_index("id", unique=True)
        logger.debug("Created unique index on books.id")

        # Index on author_id for author lookup
        await books.create_index("author_id")
        logger.debug("Created index on books.author_id")

        # Index on publisher for publisher aggregations
        await books.create_index("publisher")
        logger.debug("Created index on books.publisher")

        # Index on tags for filtering
        await books.create_index("tags")
        logger.debug("Created index on books.tags")

        # Compound index for common search patterns
        await books.create_index([("title", 1), ("author_id", 1)])
        logger.debug("Created compound index on books.title and books.author_id")

        # Authors collection indexes
        authors = cls._db["authors"]

        # Unique index on id
        await authors.create_index("id", unique=True)
        logger.debug("Created unique index on authors.id")

        # Index on name for searching
        await authors.create_index("name")
        logger.debug("Created index on authors.name")

        logger.info("Database indexes created successfully")

    @classmethod
    def get_db(cls) -> Optional[AsyncIOMotorDatabase]:
        """Get database instance."""
        return cls._db


async def get_database() -> AsyncIOMotorDatabase:
    """Dependency injection for database."""
    db = MongoDB.get_db()
    if db is None:
        raise RuntimeError("Database not initialized. Call MongoDB.connect() first.")
    return db
