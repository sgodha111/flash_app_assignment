# 📦 Book Library - Installation Guide

Step-by-step guide to install and run the application.

---

## ✅ Prerequisites

- Docker Desktop installed
- Docker Compose (included with Docker)
- ~5 GB free disk space
- Ports 8000, 8501, 27017 available

---

## 🚀 Installation (6 Steps)

### Step 1: Get the Project

```bash
git clone <repository-url>
cd book-library
```

Or extract from ZIP file.

### Step 2: Build Docker Images

```bash
docker-compose build
```

Takes 2-5 minutes on first run.

### Step 3: Start Services

```bash
docker-compose up -d
```

Starts 3 containers: MongoDB, API, Frontend

### Step 4: Wait for Services

Wait 15-20 seconds for full initialization.

### Step 5: Verify Running

```bash
docker-compose ps
```

Should show 3 containers as "Up".

### Step 6: Seed Database with Demo Data

```bash
docker-compose exec api python3 seed_db.py
```

**Expected output**:
```
✅ Seeded 5 users
✅ Seeded 3 authors
✅ Seeded 2 books

📚 Total: 10 records created!
```

**What gets created**:
- **5 Users** - Demo login accounts
- **3 Authors** - Sample authors for reference
- **2 Books** - Sample books with authors

This way users see sample data when they first login, so Authors dropdown is pre-populated and they won't see empty lists.

*Note*: Bcrypt warning may appear - this is harmless.

---

## 🧪 Run Tests (Optional - For Developers)

### Prerequisites for Testing
- Python 3.11+ installed locally
- Virtual environment (recommended)

### Setup Test Environment

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest tests/ -v
```

**Expected output**:
```
===================== 21 passed, 1 skipped =====================
```

### Run Tests with Coverage Report

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Shows code coverage percentage for each module.

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Specific test file
pytest tests/unit/test_book_service.py -v

# Specific test
pytest tests/unit/test_book_service.py::test_book_service_get_all_books -v
```

### Test Coverage Summary

- **Total Tests**: 22 (21 passing, 1 skipped)
- **Code Coverage**: 59%
- **Unit Tests**: 5 tests for BookService
- **Integration Tests**: 16 tests for API endpoints

**Skipped tests**: Login test requires real database with seeded users (runs in CI/CD pipeline)

---

## 🎉 Access Application

### First Login
```
URL: http://localhost:8501
Email: admin@example.com
Password: admin@123
```

### Other URLs
- **API**: http://localhost:8000
- **Swagger**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📋 Demo Users

All 5 users created automatically by seed_db.py:

```
admin@example.com       / admin@123
john@example.com        / john@1234
jane@example.com        / jane@1234
developer@example.com   / dev@12345
demo@example.com        / demo@1234
```

---

## 🛠️ Docker Commands

| Command | What It Does |
|---------|--------------|
| `docker-compose up -d` | Start services |
| `docker-compose down` | Stop services |
| `docker-compose ps` | Check status |
| `docker-compose logs` | View logs |
| `docker-compose restart` | Restart services |

---

## 🗑️ Cleanup & Reinstall

### Options

| Option | Command | Result |
|--------|---------|--------|
| **Pause only** | `docker-compose down` | Stop, keep data & images |
| **Fresh start** | `docker-compose down -v` | Remove data (recommended) |
| **Complete clean** | `docker-compose down -v --rmi all` | Remove all |

### Full Cleanup

```bash
# Remove everything
docker-compose down -v --rmi all

# Verify clean (should return nothing)
docker ps -a | grep book-library
docker images | grep book-library
docker volume ls | grep book-library
```

---

## 🧪 Test Troubleshooting

**Tests fail to run**
- Install test dependencies: `pip install -r requirements.txt`
- Ensure Python 3.11+ is installed: `python3 --version`

**Tests timeout or hang**
- Increase timeout: `pytest tests/ -v --timeout=30`

**Coverage report missing**
- Install coverage: `pip install pytest-cov`

**Import errors when running tests**
- Ensure you're in the project root directory
- Check virtual environment is activated

---

## ⚠️ Installation Issues

**Docker not running**
- Open Docker Desktop and wait for it to start

**Ports already in use**
- Stop other services OR change ports in docker-compose.yml

**Build fails**
- Retry: `docker-compose build`
- Check internet connection
- Verify Docker is running

**Services not starting**
- Wait 30 seconds
- Check logs: `docker-compose logs`
- Restart: `docker-compose down && docker-compose up -d`

**Database won't seed**
- Verify API is running: `docker-compose ps`
- Check logs: `docker-compose logs api`
- Retry: `docker-compose exec api python3 seed_db.py`

**Login fails after seeding**
- Try different demo user
- Check API health: http://localhost:8000/health
- Clear browser cache

---

## 🔄 Automated Testing in CI/CD

When you push code to GitHub, the CI/CD pipeline automatically runs:

1. **Formatting Check** - Black & isort
2. **Linting** - Pylint & mypy  
3. **Unit & Integration Tests** - 21 pytest tests
4. **Security Scan** - Bandit & Safety
5. **Docker Build** - Build Docker image

All steps must pass before merging to main branch.

**Check CI/CD Status**: GitHub Actions tab in your repository

---

## 📚 Next Steps

1. **Login** to dashboard: http://localhost:8501
2. **Read** [USER_GUIDE.md](USER_GUIDE.md) for dashboard guide
3. **Check** [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for quick lookup
4. **Explore** all 5 dashboard pages
5. **Run tests** to verify setup (see Testing section above)

---

## 📖 Documentation

- **README.md** - Project overview
- **USER_GUIDE.md** - Dashboard guide  
- **API_REFERENCE.md** - API documentation
- **QUICK_REFERENCE.md** - Quick lookup

---

**Installation complete! Dashboard ready at http://localhost:8501 🎉**
