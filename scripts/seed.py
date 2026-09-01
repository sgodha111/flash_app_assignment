"""Seed database with sample data."""

import asyncio
import logging
import os
from datetime import date, datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def seed_database():
    """Seed the database with sample data."""
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    database_name = os.getenv("DATABASE_NAME", "book_library")

    logger.info(f"Connecting to MongoDB at {mongo_uri}")
    client = AsyncIOMotorClient(mongo_uri)
    db = client[database_name]

    try:
        # Clear existing data
        logger.info("Clearing existing collections")
        await db["books"].delete_many({})
        await db["authors"].delete_many({})

        # Seed authors
        authors = [
            {
                "id": 1,
                "name": "Mark Lutz",
                "birth_date": datetime(1957, 1, 1, tzinfo=timezone.utc),
            },
            {
                "id": 2,
                "name": "Harry Percival",
                "birth_date": datetime(1975, 1, 1, tzinfo=timezone.utc),
            },
            {
                "id": 3,
                "name": "Bob Gregory",
                "birth_date": datetime(1978, 1, 1, tzinfo=timezone.utc),
            },
        ]

        logger.info(f"Inserting {len(authors)} authors")
        result = await db["authors"].insert_many(authors)
        logger.info(f"Inserted author IDs: {result.inserted_ids}")

        # Seed books
        books = [
            {
                "id": 1,
                "title": "Learning Python",
                "author_id": 1,
                "publisher": "O'Reilly Media",
                "pages": 1648,
                "tags": ["Python", "Development", "Learning"],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "id": 2,
                "title": "Architecture Patterns with Python",
                "author_id": 2,
                "publisher": "O'Reilly Media",
                "pages": 304,
                "tags": ["Python", "Development", "Functional Programming"],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "id": 3,
                "title": "Python Cookbook",
                "author_id": 1,
                "publisher": "O'Reilly Media",
                "pages": 656,
                "tags": ["Python", "Recipes", "Development"],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "id": 4,
                "title": "Fluent Python",
                "author_id": 1,
                "publisher": "O'Reilly Media",
                "pages": 770,
                "tags": ["Python", "Advanced", "Development"],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
            {
                "id": 5,
                "title": "Domain-Driven Design",
                "author_id": 3,
                "publisher": "Addison-Wesley",
                "pages": 560,
                "tags": ["Design", "Architecture", "Software"],
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        ]

        logger.info(f"Inserting {len(books)} books")
        result = await db["books"].insert_many(books)
        logger.info(f"Inserted book IDs: {result.inserted_ids}")

        logger.info("✅ Database seeding completed successfully")

        # Show summary
        author_count = await db["authors"].count_documents({})
        book_count = await db["books"].count_documents({})
        logger.info(f"Database contains {author_count} authors and {book_count} books")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        client.close()
        logger.info("Connection closed")


if __name__ == "__main__":
    asyncio.run(seed_database())
