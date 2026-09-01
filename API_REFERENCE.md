# 📡 Book Library API - Complete Reference

Complete API documentation for developers and advanced users.

---

## Quick Access

| Item | Location |
|------|----------|
| **Swagger UI** | http://localhost:8000/docs |
| **Redoc** | http://localhost:8000/redoc |
| **Base URL** | http://localhost:8000 |
| **Health** | http://localhost:8000/health |

---

## API Endpoints (13 Total)

### Health & Status (2)

```
GET /health
Response: {"status":"healthy","service":"Book Library API"}
Purpose: Quick health check
```

```
GET /ready
Response: {"status":"ready","database":"connected"}
Purpose: Check if API ready (database connected)
```

---

### Books Endpoints (6)

#### Get Next Book ID
```
GET /books/next-id
Response: {"next_id": 2}
Purpose: Get auto-generated ID for new book
```

#### Create Book
```
POST /books
Content-Type: application/json

Request:
{
  "title": "Book Title",
  "pages": 300,
  "author_id": 1,
  "publisher": "Publisher Name",
  "tags": ["tag1", "tag2"]
}

Response: 201 Created
{
  "id": 2,
  "title": "Book Title",
  "pages": 300,
  "author_id": 1,
  "publisher": "Publisher Name",
  "tags": ["tag1", "tag2"]
}
```

#### List Books
```
GET /books?page=1&limit=10&author_id=1&title="search"

Query Parameters:
- page: Page number (default: 1)
- limit: Items per page (default: 10)
- author_id: Filter by author (optional)
- title: Search by title (optional)

Response: 200 OK
{
  "total": 5,
  "page": 1,
  "limit": 10,
  "items": [
    {
      "id": 1,
      "title": "Book Title",
      "pages": 300,
      "author_id": 1,
      "publisher": "Publisher"
    }
  ]
}
```

#### Get Specific Book
```
GET /books/{id}

Response: 200 OK
{
  "id": 1,
  "title": "Book Title",
  "pages": 300,
  "author_id": 1,
  "publisher": "Publisher"
}
```

#### Update Book
```
PATCH /books/{id}
Content-Type: application/json

Request:
{
  "title": "New Title",
  "pages": 350
}

Response: 200 OK
{
  "id": 1,
  "title": "New Title",
  "pages": 350,
  "author_id": 1,
  "publisher": "Publisher"
}
```

#### Delete Book
```
DELETE /books/{id}

Response: 204 No Content
```

---

### Authors Endpoints (4)

#### Create Author
```
POST /authors
Content-Type: application/json

Request:
{
  "id": 1,
  "name": "Author Name",
  "birth_date": "1965-07-31"
}

Response: 201 Created
{
  "id": 1,
  "name": "Author Name",
  "birth_date": "1965-07-31"
}
```

#### Get Author
```
GET /authors/{id}

Response: 200 OK
{
  "id": 1,
  "name": "Author Name",
  "birth_date": "1965-07-31"
}
```

#### List Authors
```
GET /authors?page=1&limit=10

Response: 200 OK
{
  "total": 5,
  "page": 1,
  "limit": 10,
  "items": [
    {
      "id": 1,
      "name": "Author Name",
      "birth_date": "1965-07-31"
    }
  ]
}
```

#### Get Author's Books
```
GET /authors/{id}/books

Response: 200 OK
[
  {
    "id": 1,
    "title": "Book Title",
    "pages": 300,
    "author_id": 1,
    "publisher": "Publisher"
  }
]
```

---

### Publishers Endpoint (1)

#### Get Publisher Statistics
```
GET /publishers/{name}/average_pages

Response: 200 OK
{
  "publisher": "Bloomsbury",
  "average_pages": 320,
  "total_books": 5,
  "books": [
    {
      "title": "Harry Potter",
      "pages": 309
    }
  ]
}
```

---

## Authentication

### Getting Access Token

```
POST /auth/login
Content-Type: application/json

Request:
{
  "email": "admin@example.com",
  "password": "admin@123"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Using Token in Requests

Add to all API requests (except /auth/login, /health):

```
Headers:
Authorization: Bearer <access_token>
```

### Token Details

- **Type**: JWT (JSON Web Token)
- **Algorithm**: HS256
- **Access Token**: Expires in 24 hours
- **Refresh Token**: Expires in 7 days

### Refreshing Token

```
POST /auth/refresh
Content-Type: application/json

Request:
{
  "refresh_token": "<refresh_token>"
}

Response: 200 OK
{
  "access_token": "new_token",
  "refresh_token": "new_refresh_token",
  "token_type": "bearer"
}
```

---

## Common Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET request successful |
| 201 | Created | POST request successful |
| 204 | No Content | DELETE successful |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing token |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | ID already exists |
| 500 | Server Error | API error |

---

## Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

Example:
```json
{
  "detail": "User with email admin@example.com already exists"
}
```

---

## Testing with Swagger UI

### Access Swagger
Go to: **http://localhost:8000/docs**

### Steps to Test
1. Open Swagger UI
2. Click "Authorize" button
3. Use endpoint `/auth/login` to get token
4. Paste token in Authorization
5. Test any endpoint

### Example Test Flow
```
1. POST /auth/login
   - Email: admin@example.com
   - Password: admin@123
   - Get access_token

2. Click "Authorize"
   - Paste: Bearer <access_token>

3. GET /books
   - Execute
   - See results

4. POST /books
   - Fill body with book data
   - Execute
   - See created book
```

---

## Testing with cURL

### Login and Get Token
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin@123"}'
```

### Use Token in Request
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/books
```

### Create Book
```bash
curl -X POST http://localhost:8000/books \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Book Title",
    "pages":300,
    "author_id":1,
    "publisher":"Publisher"
  }'
```

---

## Rate Limiting

- No rate limiting currently implemented
- Production deployment should add rate limiting

---

## Pagination

All list endpoints support pagination:

```
GET /books?page=1&limit=10
GET /authors?page=2&limit=5
```

Parameters:
- `page`: Page number (starts at 1)
- `limit`: Items per page (default: 10)

Response includes:
- `total`: Total items in database
- `page`: Current page
- `limit`: Items per page
- `items`: Array of results

---

## Demo Credentials

| Email | Password |
|-------|----------|
| admin@example.com | admin@123 |
| john@example.com | john@1234 |
| jane@example.com | jane@1234 |
| developer@example.com | dev@12345 |
| demo@example.com | demo@1234 |

---

## API Health Check

### Simple Health Check
```
GET http://localhost:8000/health

Response:
{
  "status": "healthy",
  "service": "Book Library API"
}
```

### Full Readiness Check
```
GET http://localhost:8000/ready

Response:
{
  "status": "ready",
  "service": "Book Library API",
  "database": "connected",
  "collections": 3
}
```

---

## Database Schema

### Books Collection
```
{
  "_id": ObjectId,
  "id": 1,
  "title": "string",
  "pages": 300,
  "author_id": 1,
  "publisher": "string",
  "tags": ["tag1", "tag2"]
}
```

### Authors Collection
```
{
  "_id": ObjectId,
  "id": 1,
  "name": "string",
  "birth_date": "ISO date string"
}
```

### Users Collection
```
{
  "_id": ObjectId,
  "id": 1,
  "email": "string",
  "name": "string",
  "password_hash": "hashed string"
}
```

---

## Integration Examples

### JavaScript/Fetch
```javascript
async function getBooks() {
  const response = await fetch('http://localhost:8000/books', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
}
```

### Python/Requests
```python
import requests

headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/books', headers=headers)
books = response.json()
```

---

## More Information

- **Full Documentation**: See [README.md](README.md)
- **Dashboard Guide**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Quick Reference**: See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

**Ready to test? Go to http://localhost:8000/docs**
