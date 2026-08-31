# Architecture Decisions & Design Rationale

This document explains key architectural decisions made in the Antonie Book Catalog API and the reasoning behind them.

## 1. Async FastAPI with Motor (Non-Blocking I/O)

**Decision:** Use FastAPI with Motor (async MongoDB driver)

**Reasoning:**
- FastAPI is built on async/await, making it natural to use async I/O
- Motor allows non-blocking database operations without thread pool overhead
- Better scalability for I/O-bound operations (network, database)
- Single-threaded async model handles more concurrent requests per CPU core

**Trade-offs:**
- Requires understanding of async/await patterns
- All downstream code must be async-compatible
- Debugging async code can be more complex

**Alternative Considered:**
- Synchronous FastAPI with SQLAlchemy ORM
  - Simpler to understand
  - Better IDE support
  - But: Thread pool overhead, worse scalability

**Why We Chose Async:**
At scale, async provides better performance. The slight complexity cost is justified for production systems.

---

## 2. Lightweight Layered Architecture

**Decision:** Four-layer architecture: Routes → Services → Repositories → Database

```
Routes (HTTP/API)
    ↓
Services (Business Logic)
    ↓
Repositories (Data Access)
    ↓
Database (MongoDB)
```

**Reasoning:**
- **Separation of Concerns:** Each layer has a single responsibility
- **Testability:** Easy to unit test services independently
- **Maintainability:** Changes in one layer don't cascade
- **Reusability:** Services can be used by multiple routes
- **Not Over-engineered:** Avoids unnecessary abstraction

**Trade-offs:**
- 4 layers vs. 2-3 layers (simpler) vs. 6+ layers (more complex)
- More files than monolithic approach
- Each layer adds a thin performance cost

**Why Not Clean/Hexagonal Architecture?**
- Those patterns are designed for large, long-lived systems
- This API is smaller in scope
- Extra adapters/ports would add complexity without proportional benefit
- YAGNI: "You Aren't Gonna Need It"

---

## 3. MongoDB with Application-Level Integer IDs

**Decision:** Keep MongoDB's `_id` for internal use; maintain application-level integer `id` field

**Reasoning:**
- **Consistency:** Integer IDs are easier to reason about in APIs
- **Migration Safety:** Won't break if we change database later
- **User-Friendly:** Simpler client-facing IDs vs. ObjectId strings
- **Index Performance:** Integer IDs are slightly more efficient than ObjectIds
- **Unique Constraint:** Easy to enforce uniqueness on integer ID

**Implementation:**
```json
{
  "_id": ObjectId("..."),  // MongoDB internal
  "id": 1,                  // Application ID
  "title": "...",
  ...
}
```

**Alternative Considered:**
- Use only MongoDB `_id` (ObjectId)
  - Simpler: 1 ID per document
  - But: Exposes internal DB details; harder to work with

- Use auto-incrementing integers (traditional databases)
  - Simpler: No duplicates possible
  - But: Requires distributed counter logic; more complex

**Why We Chose This:**
Best balance of simplicity, API cleanliness, and safety.

---

## 4. Pydantic for Validation (Not ORM)

**Decision:** Use Pydantic schemas for validation; don't use Beanie or other ODM/ORM

**Reasoning:**
- **Explicit:** Clear separation between validation and persistence
- **Flexible:** Repository layer controls how data is stored
- **Lightweight:** No magic; straightforward to understand
- **Testing:** Mock repositories easily without ORM overhead
- **Performance:** Direct MongoDB operations without ORM translation

**Trade-off:**
- Manual mapping between Pydantic models and MongoDB documents
- More boilerplate than ORM

**Why Not Beanie/Mongoengine (ODM)?**
- For this API scope, the overhead isn't justified
- Direct `insert_one`/`find`/`update_one` is clearer
- Easier to write custom queries and aggregations
- Simpler to understand and debug

---

## 5. Repository Pattern for Data Access

**Decision:** Explicit Repository classes for each entity type

**Reasoning:**
- **Abstraction:** Database operations encapsulated in one place
- **Testability:** Repositories can be mocked in service tests
- **Consistency:** All data access goes through same interface
- **Flexibility:** Easy to swap implementations (MongoDB → SQL)
- **Query Optimization:** Centralized place to optimize queries

**Structure:**
```python
class BookRepository:
    def create(self, data) -> dict
    def get_by_id(self, id) -> dict
    def list_books(...) -> Tuple[List[dict], int]
    def update(self, id, data) -> dict
    def delete(self, id) -> bool
```

**Why Repositories Over Direct Access?**
- Routes shouldn't know MongoDB syntax
- Easier to reuse queries across services
- Single place to apply caching/optimization
- Follows dependency inversion principle

---

## 6. Service Layer for Business Logic

**Decision:** Service classes contain all business logic, validation beyond Pydantic

**Reasoning:**
- **SRP:** Services handle "what" (business rules), repos handle "how" (storage)
- **Testing:** Easy to test business logic without HTTP layer
- **Reusability:** Same logic used by multiple routes if needed
- **Validation:** Complex validation rules live here, not in routes

**Examples:**
- Check if author exists before creating book
- Ensure IDs are unique
- Handle partial updates correctly (don't overwrite unset fields)
- Calculate aggregations

---

## 7. MongoDB Aggregation for Complex Queries

**Decision:** Use MongoDB aggregation pipelines for author book count and publisher stats

**Reasoning:**
- **Efficiency:** Database does the computation, not Python
- **Scalability:** Aggregation is optimized at database level
- **Correctness:** Single source of truth; no sync issues

**Aggregation Examples:**
```python
# Author with book count
pipeline = [
    {"$lookup": {"from": "books", "localField": "id", ...}},
    {"$addFields": {"book_count": {"$size": "$books"}}},
]

# Publisher average pages
pipeline = [
    {"$match": {"publisher": "O'Reilly"}},
    {"$group": {"_id": "$publisher", "average_pages": {"$avg": "$pages"}}},
]
```

**Why Not Python?**
- Inefficient to load all books and calculate in Python
- Doesn't scale with data growth
- Database is designed for these operations

---

## 8. Streamlit for Frontend (Optional)

**Decision:** Provide Streamlit frontend that calls API (not accessing DB directly)

**Reasoning:**
- **Separation:** Frontend communicates only via REST API
- **Scalability:** Multiple frontends can use same API
- **Security:** No direct database access from UI
- **Simplicity:** Streamlit good for data apps; faster than SPA
- **Optional:** Backend works with any frontend

**Architecture:**
```
Streamlit → HTTP → FastAPI → MongoDB
```

**Alternative Considered:**
- React SPA + Redux
  - Better UX for complex interactions
  - Steeper learning curve
  - More boilerplate
  - But: Would provide better UX

**Why Streamlit for This Assignment?**
- Focuses attention on backend (FastAPI, MongoDB)
- Demonstrates API-first thinking
- Still provides working UI
- Can be replaced with React/Vue later

---

## 9. Docker Compose for Local Development

**Decision:** Single `docker-compose.yml` with API, Streamlit, and MongoDB

**Reasoning:**
- **Consistency:** Development environment matches production
- **Reproducibility:** Everyone uses same MongoDB version
- **Simplicity:** One command to start everything
- **Isolation:** No port conflicts or system dependencies

**Services:**
```yaml
api:
  build: Dockerfile
  depends_on: mongodb
  
frontend:
  build: Dockerfile.frontend
  depends_on: api
  
mongodb:
  image: mongo:7.0
  volumes: mongodb_data
```

**Why Docker?**
- No "works on my machine" problems
- Production-like environment locally
- Easy onboarding for new developers

---

## 10. Terraform Modules for Infrastructure

**Decision:** Modularize Terraform: networking, security, ALB, ECS, IAM, logging

**Reasoning:**
- **Reusability:** Modules can be reused across projects
- **Maintainability:** Changes isolated to relevant module
- **Readability:** Each module has single responsibility
- **Composability:** Combine modules for different deployments

**Modules:**
- `networking/`: VPC, subnets, NAT, IGW
- `security/`: Security groups
- `alb/`: Application Load Balancer
- `ecs/`: ECS cluster, task definition, service, auto-scaling
- `iam/`: IAM roles and policies
- `logging/`: CloudWatch logs
- `ecr/`: ECR repository

**Why Modules Over Monolithic?**
- Single 500-line `main.tf` becomes hard to navigate
- Modules roughly mirror AWS logical separation
- Easier to understand "this module handles load balancing"

---

## 11. AWS Fargate (Serverless ECS) Over EC2

**Decision:** Use AWS Fargate instead of managing EC2 instances

**Reasoning:**
- **Operational Simplicity:** AWS manages infrastructure
- **Cost:** Pay only for what you use
- **Scalability:** Auto-scaling built-in
- **Security:** Less infrastructure to secure
- **Simplicity:** No SSH to instances

**Trade-offs:**
- Slightly higher cost per GB compared to reserved instances (but more flexible)
- Less control over infrastructure
- Cold start delays (minor, ~10-30s)

**Alternative Considered:**
- EC2 with Docker
  - Full control
  - Potentially cheaper at scale
  - But: Need to manage OS, patches, security
  - Not recommended for small team

- Kubernetes (EKS)
  - More powerful
  - Overkill for this application
  - Higher operational complexity

**Why Fargate?**
For a small team, Fargate's "just run containers" simplicity wins.

---

## 12. MongoDB Atlas Over Self-Hosted

**Decision:** Terraform references MongoDB Atlas (managed cloud), not self-hosted

**Reasoning:**
- **Operations:** Atlas handles backups, updates, patches
- **High Availability:** Built-in replication and failover
- **Security:** SSL, IP whitelist, at-rest encryption
- **Scalability:** Sharding available
- **Cost:** Predictable, no DevOps overhead

**Why Not Self-Hosted?**
- Requires operational expertise
- Backups and recovery become our responsibility
- Cluster management is complex
- Not recommended for production unless you need specific control

**Note:** Terraform doesn't provision Atlas (AWS can't); only documents connection pattern.

---

## 13. GitHub Actions for CI/CD

**Decision:** Use GitHub Actions for lint, test, build, (optional deploy)

**Reasoning:**
- **Built-in:** Integrated with GitHub; no external service
- **Simple:** YAML configuration is straightforward
- **Free:** Generous free tier for public repos
- **Ecosystem:** Good community, lots of examples

**Pipeline:**
1. Lint (Black, isort, pylint)
2. Test (pytest with coverage)
3. Security (bandit, safety)
4. Build Docker image
5. Push to registry
6. (Optional) Deploy to ECS

**Why Not Jenkins/GitLab/CircleCI?**
- GitHub Actions is "good enough" and built-in
- Avoids additional service/complexity
- Easy to understand for GitHub users

---

## 14. Partial Updates (PATCH) vs Full Replacement (PUT)

**Decision:** Use PATCH for partial updates; don't implement PUT

**Reasoning:**
- **User-Friendly:** Only send fields you want to change
- **Safety:** Won't accidentally overwrite fields
- **Efficiency:** Smaller payloads
- **Database Efficiency:** Only update changed fields

**Implementation:**
```python
class BookUpdate(BaseModel):
    title: Optional[str] = None
    pages: Optional[int] = None
    # All fields optional for PATCH

@patch("/books/{book_id}")
async def update_book(id, update: BookUpdate):
    # Only include fields that were explicitly set
    update_data = update.model_dump(exclude_unset=True)
    return await service.update_book(id, update_data)
```

**Why PATCH Over PUT?**
- PUT requires sending full object (less convenient)
- PATCH is standard for partial updates in REST
- No need to implement both

---

## 15. Error Handling Strategy

**Decision:** Consistent error responses; don't expose internal errors

**Reasoning:**
- **Security:** Don't leak implementation details
- **Consistency:** Clients know what to expect
- **Debugging:** Still log full errors server-side

**Pattern:**
```python
try:
    # Try operation
except ValueError as e:
    if "not found" in str(e):
        raise HTTPException(status_code=404, detail=str(e))
    else:
        raise HTTPException(status_code=422, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}")  # Log full error
    raise HTTPException(status_code=500, detail="Internal server error")
```

**Error Response Format:**
```json
{
  "error": "Not Found",
  "detail": "Book with ID 999 not found",
  "status_code": 404
}
```

---

## 16. No Authentication in MVP

**Decision:** Skip JWT/OAuth for this assignment

**Reasoning:**
- **Scope:** Focus is backend API design, not auth
- **Simplicity:** Reduces complexity
- **Future-Ready:** Structure allows easy auth addition
- **Assignment Requirements:** Not explicitly required

**How to Add Later:**
1. Add JWT token generation endpoint
2. Add `@require_auth()` decorator to routes
3. Extract user from token in dependency
4. Add authorization checks (optional)

---

## 17. Logging Strategy

**Decision:** Structured logging; avoid logging credentials

**Reasoning:**
- **Searchability:** Structured logs are easier to parse
- **Security:** Never log passwords, tokens, connection strings
- **Observability:** Know what's happening in production

**What We Log:**
- ✅ Startup/shutdown
- ✅ Request summaries
- ✅ Database operations (counts, not data)
- ✅ Errors and exceptions
- ❌ Passwords, tokens, connection strings
- ❌ Sensitive user data

---

## 18. Database Indexes Strategy

**Decision:** Create specific indexes for actual query patterns

**Reasoning:**
- **Performance:** Faster queries
- **Cost:** Storage overhead is minimal
- **Maintenance:** Fewer indexes = less to manage

**Indexes We Create:**
- `books.id` - Unique lookup
- `books.author_id` - Author filtering
- `books.publisher` - Publisher aggregation
- `books.tags` - Tag filtering
- `books.title, author_id` - Combined search

**Why Not Index Everything?**
- Index maintenance cost during writes
- Storage overhead
- Most queries use these 5 patterns
- Can add more later if needed

---

## Summary: Design Philosophy

**Core Principles:**
1. **YAGNI:** Don't build what we don't need
2. **DRY:** Don't repeat yourself (within reason)
3. **Clarity:** Code should be easy to understand
4. **Testability:** Easy to test in isolation
5. **Production-Ready:** Not a prototype; can deploy to production
6. **Maintainability:** Future developers can understand it
7. **Performance:** Scales reasonably without over-engineering

**What Makes This Good:**
- ✅ Clear separation of concerns
- ✅ Easy to test
- ✅ Production-ready architecture
- ✅ Reasonable performance without premature optimization
- ✅ Easy to modify or extend
- ✅ Follows REST conventions

**What Could Be Better (Future):**
- Authentication/Authorization
- Caching layer (Redis)
- Rate limiting
- Advanced monitoring
- GraphQL endpoint
- Microservices (if needed)
