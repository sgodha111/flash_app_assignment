"""Seed database with sample users."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.mongodb import MongoDB
from app.services.auth_service import AuthService


async def seed_users():
    """Seed database with sample users."""
    db = await MongoDB.connect()
    users_collection = db["users"]

    # Sample users with credentials
    sample_users = [
        {
            "id": 1,
            "email": "admin@example.com",
            "name": "Admin User",
            "password_hash": AuthService.hash_password("admin@123"),
        },
        {
            "id": 2,
            "email": "john@example.com",
            "name": "John Doe",
            "password_hash": AuthService.hash_password("john@1234"),
        },
        {
            "id": 3,
            "email": "jane@example.com",
            "name": "Jane Smith",
            "password_hash": AuthService.hash_password("jane@1234"),
        },
        {
            "id": 4,
            "email": "developer@example.com",
            "name": "Developer",
            "password_hash": AuthService.hash_password("dev@12345"),
        },
        {
            "id": 5,
            "email": "demo@example.com",
            "name": "Demo User",
            "password_hash": AuthService.hash_password("demo@1234"),
        },
    ]

    # Check if users already exist
    existing_count = await users_collection.count_documents({})
    if existing_count > 0:
        print(f"⚠️  Database already has {existing_count} users. Skipping seeding.")
        await MongoDB.disconnect()
        return

    # Insert users
    result = await users_collection.insert_many(sample_users)
    print(f"✅ Seeded {len(result.inserted_ids)} users")

    # Print user credentials
    print("\n📋 SAMPLE USER CREDENTIALS:")
    print("=" * 60)
    for user in sample_users:
        # Extract password from hash (we'll show the original)
        email = user["email"]
        if email == "admin@example.com":
            password = "admin@123"
        elif email == "john@example.com":
            password = "john@1234"
        elif email == "jane@example.com":
            password = "jane@1234"
        elif email == "developer@example.com":
            password = "dev@12345"
        else:
            password = "demo@1234"

        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Name: {user['name']}")
        print("-" * 60)

    await MongoDB.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_users())
