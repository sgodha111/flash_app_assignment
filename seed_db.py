"""Database seeding script for demo users."""

import asyncio
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

from app.database.mongodb import MongoDB
from app.services.auth_service import AuthService


async def seed():
    """Seed database with 5 demo users."""
    db = await MongoDB.connect()
    users_coll = db['users']

    sample_users = [
        {
            'id': 1,
            'email': 'admin@example.com',
            'name': 'Admin User',
            'password_hash': AuthService.hash_password('admin@123')
        },
        {
            'id': 2,
            'email': 'john@example.com',
            'name': 'John Doe',
            'password_hash': AuthService.hash_password('john@1234')
        },
        {
            'id': 3,
            'email': 'jane@example.com',
            'name': 'Jane Smith',
            'password_hash': AuthService.hash_password('jane@1234')
        },
        {
            'id': 4,
            'email': 'developer@example.com',
            'name': 'Developer',
            'password_hash': AuthService.hash_password('dev@12345')
        },
        {
            'id': 5,
            'email': 'demo@example.com',
            'name': 'Demo User',
            'password_hash': AuthService.hash_password('demo@1234')
        },
    ]

    result = await users_coll.insert_many(sample_users)
    print(f"✅ Seeded {len(result.inserted_ids)} users successfully!")
    await MongoDB.disconnect()


if __name__ == '__main__':
    asyncio.run(seed())
