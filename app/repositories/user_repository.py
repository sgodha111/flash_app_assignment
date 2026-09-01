"""User repository for database operations."""

from typing import Optional

from app.database.mongodb import MongoDB


class UserRepository:
    """Repository for user database operations."""

    def __init__(self, db):
        """Initialize user repository."""
        self.db = db
        self.collection = db["users"]

    async def create_user(self, user_data: dict) -> dict:
        """Create a new user."""
        result = await self.collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return user_data

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        return await self.collection.find_one({"email": email})

    async def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """Get user by ID."""
        return await self.collection.find_one({"id": user_id})

    async def list_users(self) -> list:
        """List all users (for admin purposes)."""
        cursor = self.collection.find()
        return await cursor.to_list(length=None)

    async def user_exists(self, email: str) -> bool:
        """Check if user exists."""
        return await self.collection.find_one({"email": email}) is not None

    async def get_next_user_id(self) -> int:
        """Get the next available user ID."""
        doc = await self.collection.find_one(sort=[("id", -1)])
        return (doc["id"] + 1) if doc else 1
