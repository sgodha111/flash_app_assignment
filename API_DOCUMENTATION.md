# Book Catalog API - Complete Documentation & Testing Guide

## API Overview
The Book Catalog API is a RESTful API built with FastAPI for managing books, authors, and publishers. The API is fully documented with Swagger/OpenAPI.

### Access Points
- **Swagger UI**: http://localhost:8000/docs
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **API Base URL**: http://localhost:8000

---

## 📚 Complete API Endpoint List

### Health & Status Endpoints

#### 1. **Health Check** ✅
- **Endpoint**: `GET /health`
- **Description**: Simple health check endpoint to verify API is running
- **Response Code**: 200
- **Example**:
```bash
curl -s http://localhost:8000/health | jq .
```
**Response**:
```json
{
  "status": "healthy",
  "service": "Antonie Book Catalog API"
}
```

---

#### 2. **Readiness Check** ✅
- **Endpoint**: `GET /ready`
- **Description**: Verifies API is ready by checking database connectivity
- **Response Code**: 200
- **Example**:
```bash
curl -s http://localhost:8000/ready | jq .
```

---

### Book Endpoints

#### 3. **Get Next Book ID (Auto-Increment)** ✅ [NEW]
- **Endpoint**: `GET /books/next-id`
- **Description**: Returns the next available Book ID for auto-increment sequence
- **Response Code**: 200
- **Use Case**: Frontend calls this to display/use the next available ID without user input
- **Example**:
```bash
curl -s http://localhost:8000/books/next-id | jq .
```
**Response**:
```json
{
  "next_id": 106
}
```
**Frontend Usage** (Streamlit):
```python
next_id = client.get_next_book_id()["next_id"]
# Display: "Next Book ID: 106 (auto-generated)"
# Use in create_book call
```

---

#### 4. **Create Book** ✅
- **Endpoint**: `POST /books`
- **Description**: Create a new book with provided details
- **Response Code**: 201 (Created)
- **Request Body**:
```json
{
  "id": 106,
  "title": "The Great Gatsby",
  "author_id": 1,
  "publisher": "Penguin Books",
  "pages": 180,
  "tags": ["Fiction", "Classic", "American Literature"]
}
```
- **Example**:
```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "id": 106,
    "title": "The Great Gatsby",
    "author_id": 1,
    "publisher": "Penguin Books",
    "pages": 180,
    "tags": ["Fiction", "Classic"]
  }' | jq .
```
**Response** (201):
```json
{
  "id": 106,
  "title": "The Great Gatsby",
  "author_id": 1,
  "publisher": "Penguin Books",
  "pages": 180,
  "tags": ["Fiction", "Classic"],
  "created_at": "2026-08-31T15:03:45.123Z",
  "updated_at": "2026-08-31T15:03:45.123Z"
}
```
**Error Cases**:
- **409 Conflict**: Book ID already exists
- **422 Validation Error**: Invalid data (author_id doesn't exist, invalid pages, etc.)

---

#### 5. **Get Book by ID** ✅
- **Endpoint**: `GET /books/{book_id}`
- **Description**: Retrieve a specific book by its ID
- **Response Code**: 200 (Found), 404 (Not Found)
- **Example**:
```bash
curl -s http://localhost:8000/books/1 | jq .
```
**Response** (200):
```json
{
  "id": 1,
  "title": "Python Programming",
  "author_id": 1,
  "publisher": "O'Reilly",
  "pages": 534,
  "tags": ["Python", "Programming"],
  "created_at": "2026-08-31T14:50:00Z",
  "updated_at": "2026-08-31T14:50:00Z"
}
```

---

#### 6. **List Books (with Filtering & Pagination)** ✅
- **Endpoint**: `GET /books`
- **Description**: List all books with optional filtering and pagination
- **Query Parameters**:
  - `page`: Page number (default: 1, min: 1)
  - `limit`: Items per page (default: 10, max: 100)
  - `author_id`: Filter by author ID (optional)
  - `title`: Filter by title (partial match, case-insensitive, optional)
  - `tags`: Filter by tags (can specify multiple, optional)
- **Response Code**: 200
- **Examples**:

**a) List all books (default pagination)**:
```bash
curl -s "http://localhost:8000/books" | jq .
```

**b) Get page 2 with 20 items per page**:
```bash
curl -s "http://localhost:8000/books?page=2&limit=20" | jq .
```

**c) Filter by author ID**:
```bash
curl -s "http://localhost:8000/books?author_id=1" | jq .
```

**d) Search by title (partial match)**:
```bash
curl -s "http://localhost:8000/books?title=Python" | jq .
```

**e) Filter by tags**:
```bash
curl -s "http://localhost:8000/books?tags=Fiction&tags=Classic" | jq .
```

**f) Combined filters**:
```bash
curl -s "http://localhost:8000/books?author_id=1&title=Python&page=1&limit=10" | jq .
```

**Response** (200):
```json
{
  "items": [
    {
      "id": 1,
      "title": "Python Programming",
      "author_id": 1,
      "publisher": "O'Reilly",
      "pages": 534,
      "tags": ["Python", "Programming"],
      "created_at": "2026-08-31T14:50:00Z",
      "updated_at": "2026-08-31T14:50:00Z"
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 1
}
```

---

#### 7. **Update Book** ✅
- **Endpoint**: `PATCH /books/{book_id}`
- **Description**: Partially update a book (only provided fields are updated)
- **Response Code**: 200 (Success), 404 (Not Found), 422 (Validation Error)
- **Request Body** (all fields optional):
```json
{
  "title": "Updated Title",
  "publisher": "New Publisher",
  "pages": 200,
  "tags": ["Updated", "Tags"],
  "author_id": 2
}
```
- **Example**:
```bash
curl -X PATCH http://localhost:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Python Programming",
    "pages": 550
  }' | jq .
```
**Response** (200):
```json
{
  "id": 1,
  "title": "Advanced Python Programming",
  "author_id": 1,
  "publisher": "O'Reilly",
  "pages": 550,
  "tags": ["Python", "Programming"],
  "created_at": "2026-08-31T14:50:00Z",
  "updated_at": "2026-08-31T15:05:30.456Z"
}
```

---

#### 8. **Delete Book** ✅
- **Endpoint**: `DELETE /books/{book_id}`
- **Description**: Delete a book by ID
- **Response Code**: 204 (No Content - Success), 404 (Not Found)
- **Example**:
```bash
curl -X DELETE http://localhost:8000/books/106
```
**Response** (204): No content (successful deletion)

---

### Author Endpoints

#### 9. **Create Author** ✅
- **Endpoint**: `POST /authors`
- **Description**: Create a new author
- **Response Code**: 201
- **Request Body**:
```json
{
  "id": 5,
  "name": "Isaac Asimov",
  "birth_date": "1920-01-02"
}
```
- **Example**:
```bash
curl -X POST http://localhost:8000/authors \
  -H "Content-Type: application/json" \
  -d '{
    "id": 5,
    "name": "Isaac Asimov",
    "birth_date": "1920-01-02"
  }' | jq .
```
**Response** (201):
```json
{
  "id": 5,
  "name": "Isaac Asimov",
  "birth_date": "1920-01-02"
}
```

---

#### 10. **Get Author by ID** ✅
- **Endpoint**: `GET /authors/{author_id}`
- **Description**: Retrieve a specific author
- **Response Code**: 200, 404
- **Example**:
```bash
curl -s http://localhost:8000/authors/1 | jq .
```

---

#### 11. **List Authors (with Pagination)** ✅
- **Endpoint**: `GET /authors`
- **Description**: List all authors with pagination
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 10)
- **Response Code**: 200
- **Example**:
```bash
curl -s "http://localhost:8000/authors?page=1&limit=10" | jq .
```
**Response** (200):
```json
{
  "items": [
    {
      "id": 1,
      "name": "Mark Lutz",
      "birth_date": null
    }
  ],
  "page": 1,
  "limit": 10,
  "total": 1
}
```

---

#### 12. **Get Author's Books** ✅
- **Endpoint**: `GET /authors/{author_id}/books`
- **Description**: Get all books by a specific author
- **Response Code**: 200
- **Example**:
```bash
curl -s http://localhost:8000/authors/1/books | jq .
```
**Response** (200):
```json
[
  {
    "id": 1,
    "title": "Python Programming",
    "author_id": 1,
    "publisher": "O'Reilly",
    "pages": 534,
    "tags": ["Python"],
    "created_at": "2026-08-31T14:50:00Z",
    "updated_at": "2026-08-31T14:50:00Z"
  }
]
```

---

### Publisher Endpoints

#### 13. **Get Publisher Analytics** ✅
- **Endpoint**: `GET /publishers/{publisher_name}/average_pages`
- **Description**: Get statistics for a publisher (average pages, book count)
- **Response Code**: 200
- **Example**:
```bash
curl -s "http://localhost:8000/publishers/O'Reilly/average_pages" | jq .
```
**Response** (200):
```json
{
  "publisher": "O'Reilly",
  "average_pages": 534.0,
  "book_count": 1
}
```

---

## 🧪 Complete API Testing Guide

### Quick Test Script (Test All Endpoints)

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "=== API Testing Suite ==="

# 1. Health Check
echo -e "\n1. Health Check"
curl -s "$BASE_URL/health" | jq .

# 2. Readiness Check
echo -e "\n2. Readiness Check"
curl -s "$BASE_URL/ready" | jq .

# 3. Get Next Book ID
echo -e "\n3. Get Next Book ID"
NEXT_ID=$(curl -s "$BASE_URL/books/next-id" | jq .next_id)
echo "Next Book ID: $NEXT_ID"

# 4. List Books
echo -e "\n4. List All Books"
curl -s "$BASE_URL/books?limit=5" | jq .

# 5. Get Single Book
echo -e "\n5. Get Book by ID (1)"
curl -s "$BASE_URL/books/1" | jq .

# 6. List Authors
echo -e "\n6. List Authors"
curl -s "$BASE_URL/authors?limit=5" | jq .

# 7. Get Author's Books
echo -e "\n7. Get Author's Books (Author ID 1)"
curl -s "$BASE_URL/authors/1/books" | jq .

# 8. Publisher Analytics
echo -e "\n8. Publisher Analytics (O'Reilly)"
curl -s "$BASE_URL/publishers/O'Reilly/average_pages" | jq .

# 9. Create New Author
echo -e "\n9. Create New Author"
curl -X POST "$BASE_URL/authors" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 999,
    "name": "Test Author",
    "birth_date": "2000-01-01"
  }' | jq .

# 10. Create New Book
echo -e "\n10. Create New Book"
curl -X POST "$BASE_URL/books" \
  -H "Content-Type: application/json" \
  -d "{
    \"id\": $NEXT_ID,
    \"title\": \"Test Book\",
    \"author_id\": 1,
    \"publisher\": \"Test Publisher\",
    \"pages\": 300,
    \"tags\": [\"Test\"]
  }" | jq .

echo -e "\n=== Testing Complete ==="
```

### How to Run the Test Script:
```bash
# Save the script as test_apis.sh
chmod +x test_apis.sh
./test_apis.sh
```

---

## 📖 How to Use the APIs from Frontend

### Streamlit Frontend Integration

**1. Import the API client**:
```python
from frontend.api_client import get_client

client = get_client()
```

**2. Get next book ID**:
```python
# Automatically fetch and display next ID
next_id_response = client.get_next_book_id()
next_book_id = next_id_response.get("next_id", 1)
st.info(f"📌 Next Book ID: {next_book_id} (auto-generated)")
```

**3. Create a book without manual ID input**:
```python
book_data = {
    "id": next_book_id,  # Auto-generated, not from user input
    "title": "The Great Gatsby",
    "author_id": 1,
    "publisher": "Penguin Books",
    "pages": 180,
    "tags": ["Fiction", "Classic"]
}
client.create_book(book_data)
```

**4. List books with filters**:
```python
# List all books
books = client.list_books(page=1, limit=10)

# Filter by author
books = client.list_books(author_id=1, page=1, limit=10)

# Search by title
books = client.list_books(title="Python", page=1, limit=10)

# Filter by tags
books = client.list_books(tags=["Fiction", "Classic"], page=1, limit=10)
```

**5. Update a book**:
```python
update_data = {
    "title": "Updated Title",
    "pages": 250
}
client.update_book(book_id=1, book_data=update_data)
```

**6. Delete a book**:
```python
client.delete_book(book_id=1)
```

**7. Create an author**:
```python
author_data = {
    "id": 5,
    "name": "Isaac Asimov",
    "birth_date": "1920-01-02"
}
client.create_author(author_data)
```

**8. Get author's books**:
```python
books = client.get_author_books(author_id=1)
```

**9. Publisher analytics**:
```python
stats = client.get_publisher_average_pages("O'Reilly")
# Returns: {"publisher": "O'Reilly", "average_pages": 534.0, "book_count": 1}
```

---

## 🌐 Access Swagger UI

Open your browser and navigate to:
```
http://localhost:8000/docs
```

The Swagger UI provides:
- ✅ Interactive API testing
- ✅ Request/Response examples
- ✅ Parameter documentation
- ✅ Direct API testing with Try it Out buttons
- ✅ Schema definitions

---

## ✨ Key Features

1. **Auto-Generated Book IDs**: Get the next ID via `/books/next-id`
2. **Advanced Filtering**: Filter books by author, title, and tags
3. **Pagination Support**: Control page size and navigate results
4. **Partial Updates**: PATCH endpoint allows updating only specific fields
5. **Author-Book Relationships**: Track which books belong to which author
6. **Publisher Analytics**: Get statistics per publisher
7. **Full API Documentation**: Swagger/OpenAPI support
8. **Error Handling**: Detailed error responses (409, 404, 422, 500)

---

## 📝 Summary Table

| # | Method | Endpoint | Description | Status |
|---|--------|----------|-------------|--------|
| 1 | GET | `/health` | Health check | ✅ |
| 2 | GET | `/ready` | Readiness check | ✅ |
| 3 | GET | `/books/next-id` | Get next book ID | ✅ NEW |
| 4 | POST | `/books` | Create book | ✅ |
| 5 | GET | `/books/{id}` | Get book | ✅ |
| 6 | GET | `/books` | List books | ✅ |
| 7 | PATCH | `/books/{id}` | Update book | ✅ |
| 8 | DELETE | `/books/{id}` | Delete book | ✅ |
| 9 | POST | `/authors` | Create author | ✅ |
| 10 | GET | `/authors/{id}` | Get author | ✅ |
| 11 | GET | `/authors` | List authors | ✅ |
| 12 | GET | `/authors/{id}/books` | Author's books | ✅ |
| 13 | GET | `/publishers/{name}/average_pages` | Publisher stats | ✅ |

**Total: 13 API Endpoints** ✅ All Tested & Working

---

## 🎯 Next Steps

1. ✅ Open Swagger UI at http://localhost:8000/docs
2. ✅ Test each endpoint using "Try it Out"
3. ✅ Use the provided curl examples for automation
4. ✅ Integrate with frontend using the API client methods shown above

---

**Last Updated**: 2026-08-31 | **Version**: 1.0.0
