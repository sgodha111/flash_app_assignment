# 📡 Book Library API - Complete Reference

Complete API documentation for developers and integrations.

---

## 🚀 Quick Start

| Resource | Location |
|----------|----------|
| **Swagger UI** | http://localhost:8000/docs |
| **Redoc** | http://localhost:8000/redoc |
| **Base URL** | http://localhost:8000 |
| **Health Check** | http://localhost:8000/health |

---

## 🔐 Authentication

### Login Endpoint
```
POST /auth/login
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "admin@123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Using Token
Add to all requests (except /auth/login, /health):
```
Authorization: Bearer <access_token>
```

### Token Details
- **Type**: JWT (JSON Web Token)
- **Algorithm**: HS256
- **Access Token**: 24-hour expiry
- **Refresh Token**: 7-day expiry

### Refresh Token
```
POST /auth/refresh
{
  "refresh_token": "<refresh_token>"
}
```

---

## 📚 Endpoints (13 Total)

### Health (2 Endpoints)

**Health Check**
```
GET /health
→ {"status": "healthy", "service": "Book Library API"}
```

**Readiness Check** (includes database)
```
GET /ready
→ {"status": "ready", "database": "connected", "collections": 3}
```

---

### Books (6 Endpoints)

**Get Next Book ID**
```
GET /books/next-id
→ {"next_id": 2}
```

**List Books** (with pagination)
```
GET /books?page=1&limit=10&author_id=1&title="search"

Parameters:
- page: Page number (default: 1)
- limit: Items per page (default: 10)
- author_id: Filter by author (optional)
- title: Search by title (optional)

→ {
  "total": 5,
  "page": 1,
  "limit": 10,
  "items": [...]
}
```

**Create Book**
```
POST /books
{
  "title": "Book Title",
  "pages": 300,
  "author_id": 1,
  "publisher": "Publisher Name",
  "tags": ["tag1", "tag2"]
}
→ 201 Created
```

**Get Book**
```
GET /books/{id}
→ {Book object}
```

**Update Book**
```
PATCH /books/{id}
{
  "title": "New Title",
  "pages": 350
}
→ 200 OK
```

**Delete Book**
```
DELETE /books/{id}
→ 204 No Content
```

---

### Authors (4 Endpoints)

**Create Author**
```
POST /authors
{
  "id": 1,
  "name": "Author Name",
  "birth_date": "1965-07-31"
}
→ 201 Created
```

**Get Author**
```
GET /authors/{id}
→ {Author object}
```

**List Authors**
```
GET /authors?page=1&limit=10
→ {total, page, limit, items}
```

**Get Author's Books**
```
GET /authors/{id}/books
→ [{Book objects}]
```

---

### Publishers (1 Endpoint)

**Publisher Statistics**
```
GET /publishers/{name}/average_pages

→ {
  "publisher": "Bloomsbury",
  "average_pages": 320,
  "total_books": 5,
  "books": [{...}]
}
```

---

## 📊 HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET request successful |
| 201 | Created | POST successful |
| 204 | No Content | DELETE successful |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid token |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | ID already exists |
| 500 | Server Error | API error |

---

## 🔍 Testing

### Swagger UI
1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Use `/auth/login` to get token
4. Paste token in Authorization
5. Test any endpoint

### cURL Examples

**Login**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin@123"}'
```

**Get Books**
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/books
```

**Create Book**
```bash
curl -X POST http://localhost:8000/books \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Harry Potter",
    "pages":309,
    "author_id":1,
    "publisher":"Bloomsbury"
  }'
```

---

## 💾 Database Schema

**Books Collection**
```json
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

**Authors Collection**
```json
{
  "_id": ObjectId,
  "id": 1,
  "name": "string",
  "birth_date": "ISO date string"
}
```

**Users Collection**
```json
{
  "_id": ObjectId,
  "id": 1,
  "email": "string",
  "name": "string",
  "password_hash": "hashed string"
}
```

---

## 🔄 Pagination

All list endpoints support pagination:

```
GET /books?page=1&limit=10
GET /authors?page=2&limit=5
```

Response includes:
- `total`: Total items in database
- `page`: Current page
- `limit`: Items per page
- `items`: Array of results

---

## 📖 Response Format

**Success**
```json
{
  "id": 1,
  "title": "Book Title",
  "pages": 300,
  "author_id": 1,
  "publisher": "Publisher"
}
```

**Error**
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## 🧪 Code Examples

### JavaScript/Fetch
```javascript
const token = "your_access_token";

async function getBooks() {
  const response = await fetch('http://localhost:8000/books', {
    headers: { 'Authorization': `Bearer ${token}` }
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

## ⚙️ Configuration

**No rate limiting** currently implemented (add for production)

**CORS** enabled for cross-origin requests

**Async** operations via Motor (MongoDB async driver)

---

## 📚 Related Documentation

- **Dashboard Guide** → [USER_GUIDE.md](USER_GUIDE.md)
- **Quick Reference** → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- **Installation** → [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Project Overview** → [README.md](README.md)

---

**Ready to test? Go to http://localhost:8000/docs** 🚀
