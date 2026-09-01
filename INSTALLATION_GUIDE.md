# 📦 Book Library - Installation Guide

Complete step-by-step guide to install and run the application.

---

## Prerequisites

- Docker Desktop installed
- Docker Compose included with Docker
- ~5 GB free disk space
- Ports 8000, 8501, 27017 available

---

## Installation Steps

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

### Step 4: Wait for Initialization

Wait 15-20 seconds for services to fully start.

### Step 5: Verify Services Running

```bash
docker-compose ps
```

Should show 3 containers as "Up".

### Step 6: Seed Database with Demo Users

```bash
docker-compose exec api python3 seed_db.py
```

**Expected output:**
```
✅ Seeded 5 users successfully!
```

**Note:** You may see a bcrypt warning - this is harmless and doesn't affect seeding. The script works correctly regardless.

The `seed_db.py` file is included in the project root and creates 5 demo users automatically.

---

## Access Application

### Dashboard
**http://localhost:8501**

### API
**http://localhost:8000**

### Swagger UI
**http://localhost:8000/docs**

### Health Check
**http://localhost:8000/health**

---

## Login

**Email:** admin@example.com
**Password:** admin@123

---

## Demo Users

- admin@example.com / admin@123
- john@example.com / john@1234
- jane@example.com / jane@1234
- developer@example.com / dev@12345
- demo@example.com / demo@1234

---

## Common Commands

| Task | Command |
|------|---------|
| View logs | `docker-compose logs` |
| View API logs only | `docker-compose logs api` |
| Stop application | `docker-compose down` |
| Restart services | `docker-compose restart` |
| Check status | `docker-compose ps` |

---

## 🗑️ Cleanup & Reinstall

### Cleanup Options

| Option | Command | Result |
|--------|---------|--------|
| **Pause only** | `docker-compose down` | Stops containers, keeps data & images |
| **Fresh start** | `docker-compose down -v` | ⭐ Recommended - removes data |
| **Complete clean** | `docker-compose down -v --rmi all` | Removes images too |

### Full Cleanup Steps

```bash
# Remove everything
docker-compose down -v --rmi all

# Verify clean (should show nothing)
docker ps -a | grep book-library
docker images | grep newversion2
docker volume ls | grep newversion2
```

### Reinstall

After cleanup, repeat Installation Steps:

Then access: **http://localhost:8501**

---

## Troubleshooting

**Docker not running:**
- Open Docker Desktop

**Ports in use:**
- Change ports in docker-compose.yml

**Connection refused:**
- Wait 30 seconds for services
- Refresh browser

**Login fails:**
- Verify email spelling
- Check database is seeded

---

## Documentation

- README.md - Project overview
- USER_GUIDE.md - Dashboard guide
- API_REFERENCE.md - API docs
- QUICK_REFERENCE.md - Quick reference

---

🎉 **Installation complete! Dashboard ready at http://localhost:8501**
