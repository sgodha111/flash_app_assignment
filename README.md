# Book Library API

A production-ready REST API for managing books and authors, built with FastAPI, MongoDB, and Streamlit frontend.

## Quick Start

### Local Development with Docker Compose

```bash
# Clone the repository
git clone <repository-url>
cd book-library

# Create environment file
cp .env.example .env

# Start services
docker-compose up

# Seed database (in another terminal)
docker-compose exec api python scripts/seed.py

# Access the application
API:       http://localhost:8000
Swagger:   http://localhost:8000/docs
Frontend:  http://localhost:8501
```

## Architecture

```
┌─────────────────────────────────────────────┐
│              Users / Frontend               │
└──────────────────┬──────────────────────────┘
                   │
                   │ HTTP/REST
                   v
        ┌──────────────────────┐
        │  Streamlit Frontend  │
        │   (Port 8501)        │
        └──────────┬───────────┘
                   │
                   │ HTTP
                   v
        ┌──────────────────────┐
        │   FastAPI Backend    │
        │   (Port 8000)        │
        └──────────┬───────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        v                     v
    ┌────────────────┐  ┌────────────────┐
    │  API Routers   │  │ Service Layer  │
    └────────────────┘  └────────────────┘
        │
        v
    ┌────────────────────┐
    │ Repository Layer   │
    │  (Data Access)     │
    └────────┬───────────┘
             │
             v
         ┌───────────┐
         │ MongoDB   │
         │           │
         └───────────┘
```

### Production (AWS)

```
Internet
   │
   v
Application Load Balancer (ALB)
   │
   v
ECS Fargate Cluster
   │
   v
FastAPI Container
   │
   v
MongoDB Atlas
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI, Pydantic |
| **Database** | MongoDB (Motor async driver) |
| **API Documentation** | OpenAPI/Swagger |
| **Testing** | Pytest, Pytest-asyncio |
| **Containerization** | Docker, Docker Compose |
| **Infrastructure** | Terraform, AWS (ECS/Fargate) |
| **CI/CD** | GitHub Actions |
| **Code Quality** | Black, isort, pylint, mypy |

## Project Structure

```
.
├── app/                          # Main application
│   ├── main.py                   # FastAPI app initialization
│   ├── config.py                 # Configuration management
│   ├── database/
│   │   └── mongodb.py            # MongoDB connection & indexes
│   ├── schemas/                  # Pydantic models
│   │   ├── book.py
│   │   ├── author.py
│   │   └── error.py
│   ├── repositories/             # Data access layer
│   │   ├── book_repository.py
│   │   └── author_repository.py
│   ├── services/                 # Business logic
│   │   ├── book_service.py
│   │   ├── author_service.py
│   │   └── publisher_service.py
│   └── api/
│       └── routes/               # API endpoints
│           ├── books.py
│           ├── authors.py
│           ├── publishers.py
│           └── health.py
├── frontend/                     # Streamlit UI
│   ├── app.py
│   └── api_client.py             # HTTP client for API
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── conftest.py               # Pytest fixtures
├── scripts/
│   └── seed.py                   # Database seeding
├── terraform/                    # AWS infrastructure
│   ├── main.tf
│   ├── variables.tf
│   └── modules/
├── .github/
│   └── workflows/
│       └── ci.yml                # CI/CD pipeline
├── Dockerfile                    # FastAPI container
├── Dockerfile.frontend           # Streamlit container
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints

### Books

```
POST   /books                           Create a new book
GET    /books                           List books (with pagination & filtering)
GET    /books/{book_id}                 Get a specific book
PATCH  /books/{book_id}                 Update a book (partial)
DELETE /books/{book_id}                 Delete a book
```

### Authors

```
POST   /authors                         Create an author
GET    /authors                         List authors with book count
GET    /authors/{author_id}             Get an author
GET    /authors/{author_id}/books       Get all books by an author
```

### Publishers

```
GET    /publishers/{publisher_name}/average_pages    Get average pages by publisher
```

### Health

```
GET    /health                          Health check
GET    /ready                           Readiness check (includes DB connectivity)
```

## API Documentation

Once the API is running:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Database Schema

### Books Collection

```json
{
  "_id": ObjectId,
  "id": 1,
  "title": "Learning Python",
  "author_id": 1,
  "publisher": "O'Reilly Media",
  "pages": 1648,
  "tags": ["Python", "Development", "Learning"],
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Authors Collection

```json
{
  "_id": ObjectId,
  "id": 1,
  "name": "Mark Lutz",
  "birth_date": "1957-01-01"
}
```

## Database Indexes

Indexes are created automatically on startup:

| Collection | Field | Type | Reason |
|-----------|-------|------|--------|
| books | id | Unique | Application-level unique identifier |
| books | author_id | Regular | Author lookup performance |
| books | publisher | Regular | Publisher aggregation queries |
| books | tags | Regular | Tag filtering |
| books | title, author_id | Compound | Combined search patterns |
| authors | id | Unique | Application-level unique identifier |
| authors | name | Regular | Author name searching |

## Running the Application

### Development (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MONGO_URI="mongodb://localhost:27017"
export DATABASE_NAME="book_library"
export ENVIRONMENT="development"

# Run MongoDB (if not using Docker)
mongod --dbpath ./data

# Seed the database
python scripts/seed.py

# Start API
python -m uvicorn app.main:app --reload

# In another terminal: Start Streamlit
streamlit run frontend/app.py
```

### Docker Compose

```bash
# Start all services
docker-compose up

# Seed the database
docker-compose exec api python scripts/seed.py

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Production (AWS)

See [terraform/README.md](terraform/README.md)

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest tests/ --cov=app --cov-report=html
# View in htmlcov/index.html
```

### Unit Tests

```bash
pytest tests/unit/ -v
```

### Integration Tests

```bash
pytest tests/integration/ -v
```

### Test Categories

**Unit Tests:**
- Service layer business logic
- Validation and error handling
- Database operation isolation

**Integration Tests:**
- Full HTTP request/response cycle
- FastAPI endpoint functionality
- MongoDB operations
- Error responses and status codes

## Environment Variables

```bash
# Core
ENVIRONMENT=development|production|testing
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=book_library

# API
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
API_BASE_URL=http://localhost:8000
```

## Configuration

### Development vs Production

**Development:**
- Hot reload enabled
- Verbose logging
- CORS enabled from all origins
- Local MongoDB

**Production:**
- No hot reload
- Structured logging
- Restricted CORS
- MongoDB Atlas

### Pagination

- **Default page size:** 10
- **Maximum page size:** 100
- **Minimum page:** 1

## Filtering & Querying

### Filter by Author

```bash
GET /books?author_id=1&page=1&limit=10
```

### Filter by Title

```bash
GET /books?title=Python&page=1&limit=10
```

### Filter by Tags

```bash
GET /books?tags=Python&tags=Development&page=1&limit=10
```

### Combine Filters

```bash
GET /books?author_id=1&title=Python&page=1&limit=10
```

## Sample Requests

### Create a Book

```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "title": "Learning Python",
    "author_id": 1,
    "publisher": "O'\''Reilly Media",
    "pages": 1648,
    "tags": ["Python", "Development"]
  }'
```

### Update a Book

```bash
curl -X PATCH http://localhost:8000/books/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learning Python (Updated)",
    "pages": 1700
  }'
```

### List Books with Filters

```bash
curl "http://localhost:8000/books?author_id=1&page=1&limit=10"
```

### Get Author's Books

```bash
curl http://localhost:8000/authors/1/books
```

### Get Publisher Statistics

```bash
curl "http://localhost:8000/publishers/O'Reilly%20Media/average_pages"
```

## Error Handling

The API returns consistent error responses:

```json
{
  "error": "Not Found",
  "detail": "Book with ID 999 not found",
  "status_code": 404
}
```

### HTTP Status Codes

| Code | Scenario |
|------|----------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted (no content) |
| 400 | Bad request (invalid parameters) |
| 404 | Not found |
| 409 | Conflict (duplicate ID) |
| 422 | Validation error |
| 500 | Server error |

## MongoDB Aggregation Pipelines

### Author with Book Count

```javascript
db.authors.aggregate([
  {
    $lookup: {
      from: "books",
      localField: "id",
      foreignField: "author_id",
      as: "books"
    }
  },
  {
    $addFields: {
      book_count: { $size: "$books" }
    }
  },
  {
    $project: {
      books: 0
    }
  }
])
```

### Publisher Average Pages

```javascript
db.books.aggregate([
  {
    $match: {
      publisher: "O'Reilly Media"
    }
  },
  {
    $group: {
      _id: "$publisher",
      average_pages: { $avg: "$pages" },
      book_count: { $sum: 1 }
    }
  }
])
```

## Logging

Application logs are structured and include:

- Startup/shutdown events
- Database connection status
- Request/response summaries
- Error details (without sensitive data)
- Performance metrics

**Log files:** See `logs/` directory

**Docker logs:**
```bash
docker-compose logs -f api
```

## Development Workflow

### 1. Code Changes

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes, commit
git commit -am "Add new feature"

# Push
git push origin feature/new-feature
```

### 2. Code Quality

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint
pylint app/ tests/

# Type check
mypy app/
```

### 3. Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app
```

### 4. Pull Request & CI/CD

GitHub Actions automatically:
- Lints code
- Runs tests with coverage
- Builds Docker image
- (Optional) Deploys to AWS

## Deployment

### Local Development
```bash
docker-compose up
```

### AWS Production
See [terraform/README.md](terraform/README.md) for:
1. Infrastructure setup
2. Building Docker image
3. Pushing to ECR
4. Deploying with Terraform

### Manual Deployment

```bash
# Build image
docker build -t book-library-api:latest .

# Tag for registry
docker tag book-library-api:latest <registry>/book-library-api:latest

# Push
docker push <registry>/book-library-api:latest

# Deploy (depends on your infrastructure)
```

## Performance Considerations

1. **Database Queries:** Filtered at MongoDB level, not in Python
2. **Pagination:** Prevents loading large datasets
3. **Indexes:** Optimized for query patterns
4. **Async/Await:** Efficient I/O handling
5. **Connection Pooling:** Reused MongoDB connections

## Security

### Implementation
- ✅ Environment-based configuration
- ✅ No credentials in code
- ✅ Input validation (Pydantic)
- ✅ Controlled error messages
- ✅ Non-root Docker user
- ✅ Security groups restrict traffic

### Future Improvements
- [ ] Authentication (JWT)
- [ ] Authorization (RBAC)
- [ ] Rate limiting
- [ ] HTTPS/TLS
- [ ] API key management
- [ ] Audit logging

## Monitoring (AWS)

CloudWatch monitors:
- **Metrics:** CPU, memory, network
- **Logs:** Application logs in `/ecs/book-library`
- **Alarms:** Can be configured for thresholds

## Troubleshooting

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
docker ps | grep mongodb

# Check MongoDB logs
docker logs book-library-mongodb

# Verify connection string
echo $MONGO_URI
```

### API Not Starting
```bash
# Check logs
docker logs book-library-api

# Verify environment variables
docker-compose exec api printenv | grep MONGO
```

### Tests Failing
```bash
# Ensure test MongoDB is running
docker-compose -f docker-compose.test.yml up

# Run with verbose output
pytest tests/ -vvs
```

### Streamlit Connection Issues
```bash
# Check API is accessible
curl http://localhost:8000/health

# Check Streamlit configuration
docker logs book-library-frontend
```

## Design Decisions

### 1. **Async Database Access (Motor)**
- **Why:** Non-blocking I/O for better scalability
- **Trade-off:** Requires async/await patterns
- **Alternative:** Synchronous PyMongo (simpler, slower)

### 2. **Lightweight Layered Architecture**
- **Why:** Clear separation without over-engineering
- **Layers:** Routes → Services → Repositories → DB
- **Trade-off:** Less abstraction than clean architecture

### 3. **MongoDB with Application-Level IDs**
- **Why:** Consistent primary key across migrations
- **How:** Use integer `id` field with unique index
- **Note:** `_id` is MongoDB's internal document ID

### 4. **Streamlit Frontend (Optional)**
- **Why:** Quick UI without building SPA
- **Limitation:** Not suitable for complex frontends
- **Alternative:** React/Vue if needed

### 5. **Terraform Modules**
- **Why:** Reusable infrastructure components
- **Benefit:** Scalability and maintainability
- **Cost:** Slight learning curve

### 6. **Secrets in AWS Secrets Manager**
- **Why:** Secure credential storage
- **Access:** ECS task role retrieves secrets
- **Alternative:** Environment variables (less secure)

## Future Improvements

### Short Term
- [ ] Add HTTPS support
- [ ] Implement rate limiting
- [ ] Add more comprehensive logging
- [ ] Expand test coverage to 100%

### Medium Term
- [ ] Authentication/Authorization
- [ ] Caching layer (Redis)
- [ ] Batch operations endpoints
- [ ] Export to CSV/PDF
- [ ] Advanced search/filtering UI

### Long Term
- [ ] Microservices architecture
- [ ] Event-driven architecture
- [ ] GraphQL API
- [ ] Mobile app
- [ ] Analytics dashboard

## Contributing

1. Create feature branch
2. Make changes with tests
3. Run linting and tests
4. Create pull request
5. Get approval and merge

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [MongoDB Manual](https://docs.mongodb.com/manual/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Docker Documentation](https://docs.docker.com)

## License

Proprietary - Book Library

## Support

For questions or issues:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check logs for error messages
4. Contact the development team

---

**Last Updated:** 2024
**Version:** 1.0.0
