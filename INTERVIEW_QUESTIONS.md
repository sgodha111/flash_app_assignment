# Potential Interview Questions

This document contains questions a senior engineer at Antonie might ask about this implementation. These reflect key decisions and trade-offs.

## Architecture & Design

### Q1: Why use async FastAPI instead of Django?

**What They're Asking:** Do you understand I/O performance, async patterns, and when async is appropriate?

**Good Answers Mention:**
- FastAPI is built on async (natural fit)
- Motor allows non-blocking MongoDB operations
- Better throughput for I/O-bound operations (database, external APIs)
- Single-threaded async vs thread-per-request
- Trade-off: async/await requires careful handling

**Follow-up:** "What's the performance difference in practice?"
- Async shines with hundreds of concurrent connections
- Django with gunicorn (thread pool) uses more memory
- For <100 concurrent users, difference is minimal
- But architecture is right for future scaling

---

### Q2: Talk through your layering decision. Why not clean/hexagonal architecture?

**What They're Asking:** Do you understand architectural patterns and when to apply them?

**Good Answers Mention:**
- Clean architecture adds 6+ layers, ports, adapters
- This API is smaller in scope; doesn't justify that overhead
- YAGNI: only add layers when you need them
- 4 layers (Routes → Services → Repos → DB) is a sweet spot
- Could migrate to clean architecture if business complexity grows

**Follow-up:** "What would trigger a move to clean architecture?"
- Multiple business domains
- Complex workflows spanning multiple aggregates
- Need for multiple frontends with different logic
- Enterprise-scale team

---

### Q3: Why keep both MongoDB `_id` and application-level `id`?

**What They're Asking:** Do you think about database design and evolution?

**Good Answers Mention:**
- `_id` is MongoDB internals; `id` is API contract
- Protects API if we migrate databases later
- Integer IDs are more user-friendly than ObjectIds
- Can enforce uniqueness on `id` independently
- Shows decoupling of DB from API

**Follow-up:** "What if you wanted to use UUIDs instead?"
- Would change `id` field type, not `_id`
- Migration: Add new `id` field, backfill, drop old
- This architecture makes that easy

---

### Q4: Explain your error handling approach

**What They're Asking:** Do you think about security, debuggability, and user experience?

**Good Answers Mention:**
- Don't expose raw database errors to clients
- Log full errors server-side for debugging
- Consistent error response format
- Return appropriate HTTP status codes
- Don't leak implementation details

**Follow-up:** "What about validation errors?"
- Pydantic automatically returns 422 with field-level details
- This is good: tells client which field is wrong
- Don't include validation rules/constraints (sometimes)
- Balance between helpful and revealing

---

## Database & Queries

### Q5: Walk me through how you'd optimize the author book count query.

**What They're Asking:** Do you understand aggregation and database performance?

**Good Answer:**
- Use MongoDB aggregation pipeline
- `$lookup` to join books collection
- `$addFields` to calculate count
- Database does computation, not Python
- Scalability: O(authors × books) in MongoDB vs. O(books) in Python

**Follow-up:** "What if you had 1M authors and 10M books?"
- Python approach: load 10M books, iterate, expensive
- Aggregation: indexed lookup, instant
- With pagination: fetch 10 authors, show book counts
- This is why database operations matter

---

### Q6: Why these specific indexes?

**What They're Asking:** Do you understand query performance and index design?

**Good Answer:**
- Index on fields used in WHERE clauses
- Index on foreign keys (author_id for joins)
- Compound index for multi-field queries
- Avoid indexing every field (write overhead)
- Only index patterns we actually query

**Indexes We Have:**
- `books.id` - Unique lookup by ID
- `books.author_id` - Filter by author
- `books.publisher` - Aggregation queries
- `books.tags` - Tag filtering
- `books.title, author_id` - Combined search

**Follow-up:** "Should we index `updated_at`?"
- No current queries filter/sort on it
- Add if we implement "updated since" endpoint
- YAGNI

---

### Q7: How do you handle partial updates without overwriting fields?

**What They're Asking:** Do you understand tricky update semantics?

**Good Answer:**
```python
# Pydantic with Optional fields
class BookUpdate(BaseModel):
    title: Optional[str] = None  # Only if sent
    
# Extract only set fields
update_data = update.model_dump(exclude_unset=True)

# Only update sent fields
{"$set": update_data}
```

- `exclude_unset=True` ignores fields not provided
- MongoDB `$set` only updates specified fields
- `updated_at` is set automatically server-side

**Edge Case:** "What if someone sends `{"pages": null}`?"
- Pydantic validation catches this (if not Optional)
- MongoDB would set to null (data loss risk)
- Design choice: Should we allow null?

---

## Testing

### Q8: What's the difference between your unit and integration tests?

**What They're Asking:** Do you understand test scope and mocking?

**Good Answer:**
- **Unit:** Test services in isolation
  - Mock repositories
  - No database
  - Fast, deterministic
  - Example: `test_create_book_duplicate_id`

- **Integration:** Test full stack
  - Real MongoDB (test instance)
  - FastAPI app and HTTP
  - Slower but comprehensive
  - Example: `test_create_book_success` (full flow)

**Follow-up:** "Do you need both?"
- Yes: Unit tests catch logic errors
- Yes: Integration tests catch edge cases in real system
- Combined: good coverage with fast feedback

**Missing Tests?**
- Could add repository tests
- Could add load testing
- Could add security testing

---

### Q9: How do you handle test database isolation?

**What They're Asking:** Do you know about test data management?

**Good Answer:**
- Use separate test database
- Clear database before each test
- Use fixtures to set up known state
- Don't rely on test execution order
- Conftest provides reusable fixtures

**Our Approach:**
```python
@pytest.fixture
async def db():
    # Connect to test DB
    db = await MongoDB.connect()
    
    # Clear
    await db.client.drop_database("test")
    
    yield db
    
    # Clean up
    await db.client.drop_database("test")
```

---

### Q10: How confident are you in your tests?

**What They're Asking:** Do you know the limitations of tests you write?

**Honest Answer:**
- ✅ Happy path works (create, read, update, delete)
- ✅ Error cases handled (not found, duplicate, invalid)
- ✅ Filtering and pagination work
- ✅ Aggregations produce correct results
- ⚠️ Doesn't test concurrency issues
- ⚠️ Doesn't test performance/scalability
- ⚠️ Doesn't test MongoDB failover
- ⚠️ Doesn't test rate limiting (not implemented)

**What To Test Further:**
- Race conditions (concurrent writes to same book)
- Performance under load
- Database unavailability
- Network timeouts

---

## Operations & Deployment

### Q11: Walk me through deploying this to AWS

**What They're Asking:** Do you understand end-to-end deployment?

**Good Answer:**
1. Build Docker image locally (`docker build`)
2. Push to ECR (`docker push`)
3. Prepare MongoDB Atlas connection string
4. Create `terraform.tfvars` with image URI and MongoDB URI
5. Run `terraform apply` (provisions infrastructure)
6. ECS automatically pulls image and starts tasks
7. ALB routes traffic to healthy tasks

**Key Points:**
- Infrastructure as Code (Terraform)
- Secrets stored in AWS Secrets Manager (not in code)
- Auto-scaling on CPU/memory
- CloudWatch logging

---

### Q12: How do you handle the MongoDB connection string securely?

**What They're Asking:** Do you think about secret management?

**Good Answer:**
- **Development:** `.env` file (git-ignored)
- **Docker:** Environment variable from docker-compose
- **Production:** AWS Secrets Manager
  - Terraform creates secret
  - ECS task fetches at runtime
  - Never logged or exposed

**What NOT to Do:**
- ❌ Store in code
- ❌ Pass as CLI argument
- ❌ Log to stdout
- ❌ Commit `.env` to git

---

### Q13: How do you monitor the running application?

**What They're Asking:** Do you think about production observability?

**Good Answer:**
- **CloudWatch Logs:** See application logs, errors
- **CloudWatch Metrics:** CPU, memory, network usage
- **ALB Health:** Check if tasks are healthy
- **Application Endpoints:** `/health` and `/ready` checks

**Could Add:**
- Prometheus metrics
- Distributed tracing (X-Ray)
- Custom business metrics
- Alerts on errors

---

## Code Quality

### Q14: How do you maintain code quality as the team grows?

**What They're Asking:** Do you think about scalability of processes?

**Good Answer:**
- **Linting:** Black, isort, pylint in CI/CD
- **Testing:** Pytest before merging
- **Type Checking:** mypy (optional but recommended)
- **Code Review:** Pull requests with tests required
- **Pre-commit Hooks:** Format before commit (local)

**CI/CD Checks:**
```yaml
✓ Format check (Black)
✓ Import sorting (isort)
✓ Linting (pylint)
✓ Tests with coverage
✓ Security scans (bandit)
✓ Docker build
```

---

### Q15: You have a complex business rule. Where does it live?

**What They're Asking:** Do you understand layering and where logic belongs?

**Good Answer (Examples):**
- **Route:** Request validation, HTTP concerns only
- **Service:** Business logic, validation, orchestration
  - Example: "Can't create book without existing author"
- **Repository:** Data access patterns only
  - Example: "Query optimization, indexing strategy"

**Example: "Only staff can delete books"**
- ❌ Not in repository (doesn't know about permissions)
- ❌ Not in route (clutters HTTP layer)
- ✅ In service or middleware (permission check)

---

## Scalability & Performance

### Q16: How would you handle 10x growth in data?

**What They're Asking:** Do you think ahead about scaling?

**Good Answer:**
- **Queries:** Already use aggregation (scales well)
- **Indexes:** Already optimized for actual patterns
- **Pagination:** Prevents loading entire dataset
- **Database:** MongoDB scales horizontally (sharding)
- **API:** Fargate auto-scales on load

**Potential Bottlenecks:**
- ALB could be bottleneck
- Network I/O between API and MongoDB
- MongoDB connection pool (can increase)

**Monitoring for:**
- Slow queries
- High CPU usage
- Memory leaks
- Connection pool exhaustion

---

### Q17: How would you implement caching?

**What They're Asking:** Do you know when/how to optimize further?

**Good Answer:**
- Could add Redis for hot data
- Cache author book counts (update on book create/delete)
- Cache publisher stats
- Be careful: stale data vs. consistency trade-off

**Example:**
```python
# Check cache first
cached = await redis.get(f"author:{author_id}:books")
if cached:
    return cached

# If miss, query DB
books = await book_repo.get_by_author(author_id)

# Cache for 5 minutes
await redis.setex(key, 300, json.dumps(books))
```

**Complexity:**
- Cache invalidation is hard
- Adds Redis dependency
- Only cache if you measure the problem

---

### Q18: Database connection pooling—explain it

**What They're Asking:** Do you understand resource management?

**Good Answer:**
- Motor maintains a pool of MongoDB connections
- Reuses connections instead of creating new ones
- Default: 50 connections
- Each concurrent request gets a connection from pool
- Returned after request completes

**Why It Matters:**
- Creating connections is expensive
- Reusing is much faster
- Limited pool prevents resource exhaustion
- Can tune pool size based on load

**Failure Mode:**
- Pool exhausted → new requests wait
- If waiting too long → requests timeout
- Monitor pool usage in production

---

## Potential Problems & Solutions

### Q19: "I'm getting 503 Service Unavailable from ALB"

**What They're Asking:** Can you troubleshoot?

**Diagnostic Steps:**
1. Check CloudWatch logs for errors
2. Verify ECS task is running
3. Check task health (curl `/health`)
4. Verify security group allows port 8000
5. Check MongoDB connection

**Common Causes:**
- MongoDB connection string wrong (Secrets Manager)
- Task crashed on startup
- Security group too restrictive
- MongoDB Atlas network access not configured

---

### Q20: "Queries are slow after 1M books"

**What They're Asking:** Can you optimize?

**Diagnostic Steps:**
1. Enable MongoDB profiling
2. Check which queries are slow
3. Verify indexes are being used
4. Look for N+1 patterns (usually not in aggregation)

**Solutions:**
- Add index if missing
- Refactor query to use aggregation
- Adjust pagination limit
- Consider database sharding

**Example—Author with book count was slow?**
- Before: N queries (one per author)
- After: One aggregation query
- This is what we did

---

## Open-Ended Questions

### Q21: "What would you do differently next time?"

**Good Answers Show:**
- Reflection on trade-offs
- Learning from this experience
- Not defensive about choices
- Practical improvements

**Honest Answers:**
- Would add authentication from day 1
- Would add more load testing
- Would document API changes in CHANGELOG
- Would add request ID for tracing
- Would implement health checks more robustly

---

### Q22: "How would you explain this architecture to a new team member?"

**What They're Asking:** Can you communicate clearly?

**Good Approach:**
1. Start with the 30-second overview
2. Walk through a request (create book)
3. Show how each layer contributes
4. Explain why we made key decisions
5. Offer to pair on their first task

---

### Q23: "What's a limitation of this design?"

**What They're Asking:** Do you know when this design breaks?

**Honest Answers:**
- Not suitable for real-time collaborative editing
- Doesn't handle complex ACID transactions well
- No built-in caching (would add Redis)
- No authentication (would need to add)
- Streamlit frontend is simple (would replace with React for complex UIs)
- Terraform doesn't provision MongoDB (managed service)

---

## Follow-up Technical Questions

### Q24: "How do you handle database migrations?"

**This Assignment:** We haven't needed them (schema-less MongoDB)

**In Production:**
- MongoDB migrations are different from SQL
- Use versioned migration scripts
- Example: Add `birth_date` field to authors
- Script: loop authors, set default date, save
- Can be done gradually (not blocking)

---

### Q25: "What about data validation at the DB level?"

**Good Answer:**
- MongoDB 4.4+ supports JSON Schema validation
- Could add to collection creation
- Pydantic validates in application
- Database validation is defense in depth

**Our Approach:**
- Pydantic on write
- Repository ensures data integrity
- Could add DB schema validation (optional)

---

## Questions They Might Ask You

### Q26: "Tell us about a time you scaled a system"

**What They're Asking:** Real experience with production systems

**Structure a Good Answer:**
1. Context: What was the system? Why scaling needed?
2. Problem: What was the bottleneck?
3. Solution: What did you change?
4. Measurement: How did you know it worked?
5. Lesson: What did you learn?

---

### Q27: "How do you approach a production incident?"

**What They're Asking:** Can you think clearly under pressure?

**Good Approach:**
1. **Detect:** Monitoring alerts you to problem
2. **Understand:** Check logs, metrics, recent changes
3. **Mitigate:** Reduce impact (scale up, route around)
4. **Fix:** Root cause analysis, deploy fix
5. **Retrospect:** Post-mortem to prevent recurrence

---

### Q28: "What's a mistake you made and what did you learn?"

**What They're Asking:** Can you learn and don't blame others?

**Good Answer:**
- Specific example (not vague)
- How you identified it
- What you changed
- What you learned
- How you'd handle it differently now

---

## Answer Quality Framework

### Strong Answers Demonstrate:
✅ Understanding the "why" not just "how"
✅ Trade-offs considered
✅ Practical experience
✅ Willingness to learn
✅ Clear communication
✅ Testing and verification
✅ Production thinking (monitoring, scale, reliability)

### Weak Answers Have:
❌ Only technical correctness, no context
❌ "I did X because it's best practice" (no reasoning)
❌ Defensive about choices
❌ No consideration of alternatives
❌ Ignoring non-functional requirements
❌ No evidence of testing/validation
