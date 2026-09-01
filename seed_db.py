"""Database seeding script for demo users, authors, and books."""

import asyncio
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

from app.database.mongodb import MongoDB
from app.services.auth_service import AuthService


async def seed():
    """Seed database with demo users, authors, and books."""
    db = await MongoDB.connect()
    users_coll = db['users']
    authors_coll = db['authors']
    books_coll = db['books']

    # Seed users
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

    # Seed authors
    sample_authors = [
        {
            'id': 1,
            'name': 'Mark Lutz',
            'birth_date': None
        },
        {
            'id': 2,
            'name': 'Harry Percival',
            'birth_date': None
        },
        {
            'id': 3,
            'name': 'Bob Gregory',
            'birth_date': None
        },
    ]

    # Seed books
    sample_books = [
        {
            'id': 1,
            'title': 'Learning Python',
            'pages': 1648,
            'author_id': 1,
            'publisher': "O'Reilly Media",
            'tags': ['Python', 'Development', 'Learning']
        },
        {
            'id': 2,
            'title': 'Architecture Patterns with Python',
            'pages': 304,
            'author_id': 2,
            'publisher': "O'Reilly Media",
            'tags': ['Python', 'Development', 'Architecture']
        },
    ]

    # Insert all data
    users_result = await users_coll.insert_many(sample_users)
    authors_result = await authors_coll.insert_many(sample_authors)
    books_result = await books_coll.insert_many(sample_books)

    print(f"✅ Seeded {len(users_result.inserted_ids)} users")
    print(f"✅ Seeded {len(authors_result.inserted_ids)} authors")
    print(f"✅ Seeded {len(books_result.inserted_ids)} books")
    print(f"\n📚 Total: {len(users_result.inserted_ids) + len(authors_result.inserted_ids) + len(books_result.inserted_ids)} records created!")

    await MongoDB.disconnect()


if __name__ == '__main__':
    asyncio.run(seed())
