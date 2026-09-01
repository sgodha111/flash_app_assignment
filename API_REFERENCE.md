# 📚 Book Catalog API - Complete Reference Guide

## 🚀 Quick Start

**Frontend**: http://localhost:8501  
**Swagger API Docs**: http://localhost:8000/docs  
**API Base URL**: http://localhost:8000

---

## 📋 All API Endpoints (13 Total)

### Health & Status (2)
```
GET /health                          → Check if API is running
GET /ready                           → Check if database is connected
```

### Books Management (6)
```
GET  /books/next-id                  → Get next sequential book ID ⭐ NEW
POST /books                          → Create new book
GET  /books                          → List books (with filters & pagination)
GET  /books/{id}                     → Get specific book
PATCH /books/{id}                    → Update book
DELETE /books/{id}                   → Delete book
```

### Authors Management (4)
```
POST /authors                        → Create author
GET  /authors/{id}                   → Get author by ID
GET  /authors                        → List authors
GET  /authors/{id}/books             → Get all books by author
```

### Publishers (1)
```
GET /publishers/{name}/average_pages → Get publisher statistics
```

---

## 🔗 Important URLs

### Main Access Points
| Purpose | URL |
|---------|-----|
| Frontend App | http://localhost:8501 |
| Swagger UI | http://localhost:8000/docs |
| API Base | http://localhost:8000 |
| Health Check | http://localhost:8000/health |
| Next Book ID | http://localhost:8000/books/next-id |

### Example URLs
```bash
# List all books
http://localhost:8000/books

# List with pagination
http://localhost:8000/books?page=2&limit=20

# Filter by author
http://localhost:8000/books?author_id=1

# Search by title
http://localhost:8000/books?title=Python

# Filter by tags
http://localhost:8000/books?tags=Fiction&tags=Classic

# Get specific book
http://localhost:8000/books/1

# Get author's books
http://localhost:8000/authors/1/books
```

---

## 💻 API Usage Examples

### Using cURL

**Get Next Book ID**
```bash
curl -s http://localhost:8000/books/next-id | jq .
```

**Create Book**
```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "id": 107,
    "title": "The Great Gatsby",
    "author_id": 1,
    "publisher": "Penguin Books",
    "pages": 180,
    "tags": ["Fiction", "Classic"]
  }' | jq .
```

**List Books**
```bash
curl -s "http://localhost:8000/books?limit=10" | jq .
```

**Update Book**
```bash
curl -X PATCH http://localhost:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "pages": 200}' | jq .
```

**Delete Book**
```bash
curl -X DELETE http://localhost:8000/books/1
```

### Using Python/Streamlit
```python
from frontend.api_client import get_client

client = get_client()

# Get next ID
next_id = client.get_next_book_id()["next_id"]

# Create book
book = client.create_book({
    "id": next_id,
    "title": "Book Title",
    "author_id": 1,
    "publisher": "Publisher",
    "pages": 300,
    "tags": ["tag1", "tag2"]
})

# List books
books = client.list_books(page=1, limit=10)
books = client.list_books(author_id=1)
books = client.list_books(title="Python")

# Update book
client.update_book(book_id=1, book_data={"title": "New Title"})

# Delete book
client.delete_book(book_id=1)

# Get author's books
books = client.get_author_books(author_id=1)

# Publisher stats
stats = client.get_publisher_average_pages("Penguin")
```

---

## 📖 How to Use Swagger UI

1. **Open**: http://localhost:8000/docs
2. **Find Endpoint**: Scroll to find what you need
3. **Click "Try it Out"**: Enables the testing form
4. **Enter Parameters**: Fill in required fields
5. **Click "Execute"**: Send request
6. **View Response**: See result in Response section

### Common Swagger Tests
- **Health**: GET /health → Click Execute → See {"status": "healthy"}
- **Next ID**: GET /books/next-id → Click Execute → See {"next_id": 107}
- **List Books**: GET /books → Optional filters → Click Execute
- **Create Book**: POST /books → Enter book data → Click Execute

---

## 🎯 Key Features

✅ **Auto-Generated Book IDs** - Sequential IDs (1, 2, 3, ...)  
✅ **Advanced Filtering** - By author, title, tags  
✅ **Pagination** - Browse large datasets  
✅ **Form Data Preservation** - Data stays on errors  
✅ **Real-time Statistics** - Live book/author counts  
✅ **Interactive Docs** - Swagger UI for testing  

---

## 📊 Quick Statistics

| Item | Value |
|------|-------|
| Total Endpoints | 13 |
| Total Books | 9 |
| Total Authors | 5 |
| Auto-ID Support | ✅ Yes |
| API Status | ✅ Healthy |
| Database | ✅ Connected |

---

## 🔐 Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Book retrieved |
| 201 | Created | Book created |
| 204 | No Content | Book deleted |
| 400 | Bad Request | Invalid parameters |
| 404 | Not Found | Book doesn't exist |
| 409 | Conflict | Duplicate book ID |
| 422 | Validation Error | Invalid data |
| 500 | Server Error | Unexpected error |

---

## 📝 Frontend Pages

| Page | URL | Purpose |
|------|-----|---------|
| 📖 Books | http://localhost:8501 | View/search books |
| ✍️ Create Book | Click in sidebar | Add new book (auto ID) |
| 👥 Authors | Click in sidebar | Manage authors |
| 🏢 Publishers | Click in sidebar | Publisher stats |
| 📋 Info & Links | Click in sidebar | This reference + Swagger access |

---

## ✅ Verification Checklist

- [ ] Frontend loads: http://localhost:8501
- [ ] API healthy: http://localhost:8000/health
- [ ] Database connected: http://localhost:8000/ready
- [ ] Swagger accessible: http://localhost:8000/docs
- [ ] Can get next ID: http://localhost:8000/books/next-id
- [ ] Can list books: http://localhost:8000/books
- [ ] Can create book: Use frontend form
- [ ] Can test APIs: Use Swagger

---

**Version**: 1.0.0 | **Last Updated**: 2026-08-31 | **Status**: ✅ Production Ready
