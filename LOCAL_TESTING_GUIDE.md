# Local Testing Guide

## Prerequisites

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Option 1: Run Tests (No MongoDB Required)

Tests use an in-memory test fixture approach. Run the entire test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_book_service.py -v

# Run specific test
pytest tests/unit/test_book_service.py::TestBookService::test_create_book_success -v
```

### Test Output
You should see:
```
tests/unit/test_book_service.py::TestBookService::test_create_book_success PASSED
tests/unit/test_book_service.py::TestBookService::test_create_book_duplicate_id PASSED
tests/integration/test_books_api.py::TestCreateBook::test_create_book_success PASSED
...
================== 39 passed in 2.45s ==================
```

## Option 2: Run API Server Locally (Requires MongoDB)

### Start MongoDB
Option A - Using Docker (if available):
```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

Option B - Using Homebrew (if installed):
```bash
brew services start mongodb-community
```

### Start FastAPI Server
```bash
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Seed Database
In another terminal:
```bash
source venv/bin/activate
python scripts/seed.py
```

### Test API with curl

#### Health Check
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "service": "Antonie Book Catalog API"}
```

#### Get Swagger Docs
```bash
# Open browser to: http://localhost:8000/docs
# Interactive API documentation
```

#### List Books
```bash
curl http://localhost:8000/books
```

#### Create Book
```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "id": 100,
    "title": "Test Book",
    "author_id": 1,
    "publisher": "Test Publisher",
    "pages": 250,
    "tags": ["test"]
  }'
```

#### Get Book
```bash
curl http://localhost:8000/books/1
```

#### Update Book
```bash
curl -X PATCH http://localhost:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

#### Delete Book
```bash
curl -X DELETE http://localhost:8000/books/100
```

#### Filter by Author
```bash
curl "http://localhost:8000/books?author_id=1"
```

#### Filter by Title
```bash
curl "http://localhost:8000/books?title=Learning"
```

#### Filter by Tags
```bash
curl "http://localhost:8000/books?tags=Python"
```

#### Pagination
```bash
curl "http://localhost:8000/books?page=1&limit=5"
```

#### Get Authors
```bash
curl http://localhost:8000/authors
```

#### Get Author's Books
```bash
curl http://localhost:8000/authors/1/books
```

#### Get Publisher Stats
```bash
curl "http://localhost:8000/publishers/O'Reilly%20Media/average_pages"
```

## Option 3: Run Streamlit Frontend

Requires API server to be running (Option 2).

```bash
source venv/bin/activate
streamlit run frontend/app.py
```

Then open browser to: http://localhost:8501

You can:
- Browse books with pagination
- Search by title
- Filter by author
- Create/update/delete books
- View authors and their books
- See publisher statistics

## Testing Workflow

### Quick Smoke Test (1 minute)
```bash
# Run tests only
pytest tests/ -v --tb=short
```

### Full Test with Coverage (3 minutes)
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### API Testing (requires MongoDB)
```bash
# Terminal 1: Start API
python -m uvicorn app.main:app --reload

# Terminal 2: Seed DB
python scripts/seed.py

# Terminal 3: Run curl commands
curl http://localhost:8000/books
```

## Troubleshooting

### "Cannot connect to MongoDB"
- Ensure MongoDB is running (check `mongosh` or docker)
- Verify MONGO_URI environment variable
- For tests: they don't need MongoDB, they use fixtures

### "Port 8000 already in use"
```bash
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### "Import errors"
```bash
# Ensure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Tests failing with connection errors
- This is normal if MongoDB isn't running
- Tests that need DB use fixtures which handle isolation
- Run: `pytest tests/ -v -s` for verbose output

## Key Test Categories

### Unit Tests (No DB needed)
- `tests/unit/test_book_service.py` - Business logic

### Integration Tests (Needs test MongoDB)
- `tests/integration/test_books_api.py` - Book API endpoints
- `tests/integration/test_authors_api.py` - Author endpoints
- `tests/integration/test_publishers_api.py` - Publisher aggregation

## API Documentation

Once the server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Next Steps

1. **Run Tests First** (no MongoDB needed):
   ```bash
   pytest tests/ -v
   ```

2. **Try the API** (with MongoDB):
   ```bash
   # Terminal 1
   python -m uvicorn app.main:app --reload
   
   # Terminal 2
   python scripts/seed.py
   
   # Terminal 3
   curl http://localhost:8000/books
   ```

3. **Explore Swagger Docs**:
   - Open http://localhost:8000/docs
   - Try requests directly in the UI

4. **Try the Frontend** (with API running):
   ```bash
   streamlit run frontend/app.py
   ```

## Tips

- Use `--tb=short` flag for cleaner pytest output
- Use `-v` for verbose test names
- Use `-s` to see print statements in tests
- Use `--lf` to run only last failed tests
- Use `-k "pattern"` to run tests matching pattern
