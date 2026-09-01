# 🔐 Authentication Setup Guide

## Overview

This Book Catalog API includes JWT-based authentication for production-ready security. All endpoints (except `/docs`, `/redoc`, and auth endpoints) require a valid JWT token.

---

## Sample Users

The application comes with 5 pre-seeded users for testing:

| # | Email | Password | Name | Role |
|---|-------|----------|------|------|
| 1 | admin@example.com | admin@123 | Admin User | Administrator |
| 2 | john@example.com | john@1234 | John Doe | Regular User |
| 3 | jane@example.com | jane@1234 | Jane Smith | Regular User |
| 4 | developer@example.com | dev@12345 | Developer | Developer |
| 5 | demo@example.com | demo@1234 | Demo User | Demo User |

---

## Getting Started

### 1. Start the Application

```bash
docker-compose up
```

### 2. Seed Users (First Time Only)

```bash
docker-compose exec api python scripts/seed_users.py
```

Or in Python environment:
```bash
python scripts/seed_users.py
```

**Output:**
```
✅ Seeded 5 users

📋 SAMPLE USER CREDENTIALS:
============================================================
Email: admin@example.com
Password: admin@123
Name: Admin User
------------------------------------------------------------
Email: john@example.com
Password: john@1234
Name: John Doe
------------------------------------------------------------
...
```

---

## Authentication Flow

### Step 1: Login (Get Tokens)

**Endpoint:** `POST /auth/login`

**Request:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin@123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 2: Use Access Token

Store the `access_token` and use it for authenticated requests:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/books
```

### Step 3: Refresh Token (When Expired)

**Endpoint:** `POST /auth/refresh`

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "YOUR_REFRESH_TOKEN"
  }'
```

---

## API Endpoints

### Authentication Endpoints (Public)

```
POST   /auth/register           Register a new user
POST   /auth/login              Login and get tokens
POST   /auth/refresh            Refresh access token
GET    /auth/me                 Get current user profile (requires auth)
```

### Protected Endpoints (Require JWT)

All other endpoints require authorization header:

```
GET    /books                   List books
POST   /books                   Create book
GET    /books/{id}              Get book
PATCH  /books/{id}              Update book
DELETE /books/{id}              Delete book

GET    /authors                 List authors
POST   /authors                 Create author
GET    /authors/{id}            Get author
GET    /authors/{id}/books      Get author's books

GET    /publishers/{name}/average_pages    Get publisher stats

GET    /health                  Health check (public)
GET    /ready                   Readiness check (public)
```

---

## Using with Frontend

The Streamlit frontend automatically:
1. Shows login page if not authenticated
2. Stores tokens in session state
3. Includes Authorization header in all API requests
4. Refreshes token automatically when expired

### Login to Frontend

1. Navigate to http://localhost:8501
2. Enter credentials from the table above
3. Click "Login"
4. Use the application normally

---

## Token Details

### Access Token
- **Expiration:** 24 hours (configurable)
- **Usage:** API requests
- **Header:** `Authorization: Bearer {token}`

### Refresh Token
- **Expiration:** 7 days (configurable)
- **Usage:** Get new access token
- **Endpoint:** `POST /auth/refresh`

### Token Payload

```json
{
  "user_id": 1,
  "email": "admin@example.com",
  "exp": 1700000000,
  "type": "access"
}
```

---

## Configuration

JWT settings in `app/config.py`:

```python
JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
JWT_ALGORITHM: str = "HS256"
JWT_EXPIRATION_HOURS: int = 24
JWT_REFRESH_EXPIRATION_DAYS: int = 7
```

### Production Deployment

⚠️ **IMPORTANT:** Change `JWT_SECRET_KEY` in production!

```bash
export JWT_SECRET_KEY="generate-a-strong-random-key-min-32-chars"
```

Generate a strong key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Testing Authentication

### Manual Test Sequence

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin@123"}' \
  | jq -r '.access_token')

# 2. Get current user
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/auth/me

# 3. Create a book
curl -X POST http://localhost:8000/books \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "title": "Test Book",
    "author_id": 1,
    "publisher": "Test",
    "pages": 100
  }'

# 4. List books
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/books
```

### Automated Tests

```bash
# Run tests with authentication
pytest tests/ -v -s

# Test auth specifically
pytest tests/ -k auth -v
```

---

## Error Handling

### Missing Authorization Header

**Status:** 403  
**Response:**
```json
{
  "detail": "Not authenticated"
}
```

### Invalid Token

**Status:** 401  
**Response:**
```json
{
  "detail": "Invalid or expired token"
}
```

### User Not Found

**Status:** 401  
**Response:**
```json
{
  "detail": "User not found"
}
```

### Invalid Credentials

**Status:** 401  
**Response:**
```json
{
  "detail": "Invalid email or password"
}
```

---

## Troubleshooting

### Users Not Seeding

Check MongoDB is running:
```bash
docker-compose ps
```

Verify database connection:
```bash
docker-compose logs api
```

### Login Fails

Ensure users are seeded:
```bash
docker-compose exec api python scripts/seed_users.py
```

Check email and password spelling (case-sensitive)

### Token Expired

Use refresh token to get new access token:
```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"YOUR_REFRESH_TOKEN"}'
```

---

## Security Best Practices

✅ **Implemented:**
- Passwords hashed with bcrypt
- JWT tokens with expiration
- Refresh token rotation
- No credentials in logs
- HTTPOnly cookies support (can be added)
- CORS configured (can be restricted)

### Recommendations for Production

1. **HTTPS/TLS** - Use SSL certificates
2. **Rate Limiting** - Prevent brute force attacks
3. **CORS Restriction** - Only allow trusted origins
4. **API Key Rotation** - Regularly rotate JWT secret
5. **Audit Logging** - Log all authentication events
6. **2FA** - Add two-factor authentication

---

## API Examples

### Complete Login & Use Flow

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@example.com",
    "password": "admin@123"
})
tokens = response.json()
access_token = tokens["access_token"]

# 2. Get current user
response = requests.get(
    f"{BASE_URL}/auth/me",
    headers={"Authorization": f"Bearer {access_token}"}
)
print(response.json())

# 3. Create a book
response = requests.post(
    f"{BASE_URL}/books",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "id": 1,
        "title": "Learning Python",
        "author_id": 1,
        "publisher": "O'Reilly",
        "pages": 1648
    }
)
print(response.json())

# 4. Refresh token
response = requests.post(
    f"{BASE_URL}/auth/refresh",
    json={"refresh_token": tokens["refresh_token"]}
)
new_tokens = response.json()
print(new_tokens)
```

---

## Environment Variables

```bash
# Required for production
JWT_SECRET_KEY=your-secret-key-min-32-chars

# Optional (defaults shown)
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
JWT_REFRESH_EXPIRATION_DAYS=7
```

---

## Documentation Links

- [JWT (JSON Web Tokens)](https://jwt.io)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python-Jose](https://github.com/mpdavis/python-jose)
- [Passlib](https://passlib.readthedocs.io/)

---

**Version:** 1.0.0  
**Last Updated:** 2026-08-31  
**Status:** Production Ready ✅
