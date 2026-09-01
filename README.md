# 📚 Book Library - Complete Application

A production-ready REST API and web dashboard for managing books, authors, and publishers.

**Built with**: FastAPI • MongoDB • Streamlit • Docker

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Start Application
```bash
docker-compose up -d
```

### Step 2: Access Dashboard
**http://localhost:8501**

### Step 3: Login with Demo Account
```
Email: admin@example.com
Password: admin@123
```

**That's it!** Dashboard loads with sample authors and books ready to explore.

---

## 📱 Access Points

| Service | URL |
|---------|-----|
| **Dashboard** | http://localhost:8501 |
| **API Swagger** | http://localhost:8000/docs |
| **API Health** | http://localhost:8000/health |
| **API Redoc** | http://localhost:8000/redoc |

---

## 🏗️ Architecture

```
Streamlit Frontend (8501)
        ↓
   FastAPI Backend (8000)
        ↓
  MongoDB Database (27017)
```

**3 Services**: Frontend, Backend API, Database (containerized)

---

## 📋 Dashboard Features

**5 Main Pages**:
- **📖 Books** - Search, filter, browse all books (with pagination)
- **✍️ Create Book** - Add new books (author required)
- **👥 Authors** - Manage authors with optional birth dates
- **🏢 Publishers** - View publisher statistics and metrics
- **📋 Info & Links** - API documentation & health status

---

## 📡 API

**13 Total Endpoints**:
- 6 Books endpoints (CRUD + pagination)
- 4 Authors endpoints (CRUD + list books)
- 1 Publisher endpoint (statistics)
- 2 Health check endpoints

**Authentication**: JWT tokens (24-hour expiry, 7-day refresh)

→ Full API docs: [API_REFERENCE.md](API_REFERENCE.md)

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI 0.100+ |
| **Database** | MongoDB 7.0 |
| **Frontend** | Streamlit 1.28+ |
| **Container** | Docker & Docker Compose |
| **Auth** | JWT + Bcrypt |
| **Async** | Motor (async MongoDB driver) |

---

## 📁 Project Structure

```
.
├── README.md                    ← You are here
├── INSTALLATION_GUIDE.md        ← Setup instructions
├── USER_GUIDE.md               ← Dashboard guide
├── API_REFERENCE.md            ← API documentation
├── QUICK_REFERENCE.md          ← One-page cheat sheet
├── DOCUMENTATION_INDEX.md      ← Navigation guide
├── docker-compose.yml          ← Container config
├── Dockerfile                  ← API container
├── Dockerfile.frontend         ← Frontend container
│
├── app/                        ← Backend (FastAPI)
│   ├── main.py
│   ├── database/
│   ├── api/routes/
│   ├── schemas/
│   └── services/
│
├── frontend/                   ← Frontend (Streamlit)
│   └── app.py
│
└── seed_db.py                 ← Demo data seeding script
```

---

## ✨ Key Features

✅ **CRUD Operations** - Create, read, update, delete books  
✅ **Advanced Search** - Real-time title search  
✅ **Filtering** - Filter books by author  
✅ **Pagination** - Browse large datasets  
✅ **Analytics** - Publisher statistics & metrics  
✅ **JWT Security** - Token-based authentication  
✅ **Pre-loaded Data** - 5 users, 3 authors, 2 books  
✅ **Multi-user** - Each user has independent session  
✅ **Docker Ready** - One-command deployment  
✅ **Responsive** - Desktop and tablet compatible  
✅ **API Testing** - Swagger UI included  
✅ **Data Persistent** - MongoDB volume storage  

---

## 📊 Pre-seeded Data

Application comes with sample data for immediate exploration:

**Users** (5 demo accounts):
- All with full CRUD access
- Passwords hashed with bcrypt

**Authors** (3 sample):
- Mark Lutz
- Harry Percival
- Bob Gregory

**Books** (2 sample):
- "Learning Python" (1648 pages)
- "Architecture Patterns with Python" (304 pages)

→ See demo credentials below for login details

---

## 🔐 Demo Credentials

5 pre-seeded users for testing:

```
admin@example.com       / admin@123
john@example.com        / john@1234
jane@example.com        / jane@1234
developer@example.com   / dev@12345
demo@example.com        / demo@1234
```

All users have full access to all features.

---

## 💻 System Requirements

**Minimum**:
- 2 GB RAM
- 5 GB disk space
- Docker & Docker Compose
- Modern browser (Chrome, Firefox, Safari, Edge)

**Recommended**:
- 4 GB RAM
- 10 GB disk space
- SSD storage
- Latest Chrome or Firefox

---

## 📚 Documentation

| File | Purpose | Read Time |
|------|---------|-----------|
| **README.md** | Project overview (this file) | 5 min |
| **INSTALLATION_GUIDE.md** | Setup & installation steps | 5 min |
| **USER_GUIDE.md** | Complete dashboard guide | 15 min |
| **API_REFERENCE.md** | API endpoints & integration | 10 min |
| **QUICK_REFERENCE.md** | One-page cheat sheet | 2 min |
| **DOCUMENTATION_INDEX.md** | Navigation & reading paths | 5 min |

**Getting Started**:
1. First time? → Start with [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
2. Want to use dashboard? → Read [USER_GUIDE.md](USER_GUIDE.md)
3. Building with API? → Check [API_REFERENCE.md](API_REFERENCE.md)
4. Need quick help? → See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
5. Lost? → Read [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| **"Connection error"** | Check API health: http://localhost:8000/health |
| **"Author not in dropdown"** | Create author first on Authors page |
| **"Login fails"** | Verify email/password (case-sensitive) |
| **"No books found"** | Create books via Create Book page |
| **"Page frozen"** | Refresh (Ctrl+R) or check API health |
| **Docker won't start** | Ensure Docker Desktop is running |

→ More help: [USER_GUIDE.md](USER_GUIDE.md) → Troubleshooting

---

## 📝 Example Workflow (5 Minutes)

```
1. Login (30 sec)
   Email: admin@example.com
   Password: admin@123

2. Explore Sample Data (1 min)
   - Go to 📖 Books → See 2 sample books
   - Go to 👥 Authors → See 3 sample authors
   - Go to 🏢 Publishers → View statistics

3. Create New Author (1 min)
   - 👥 Authors → + Add New Author
   - ID: 100, Name: Your Author Name

4. Create New Book (1.5 min)
   - ✍️ Create Book
   - Title: Your Book Title
   - Select your author from dropdown
   - Click ✨ Create Book

5. Verify (1 min)
   - 📖 Books → Search for your book
   - 🏢 Publishers → Select publisher → View stats
```

---

## 🚀 Next Steps

- **Installing?** → Follow [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **Using dashboard?** → Read [USER_GUIDE.md](USER_GUIDE.md)
- **Building API integration?** → Check [API_REFERENCE.md](API_REFERENCE.md)
- **Quick lookup needed?** → See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 💾 Data Persistence

- **Database**: MongoDB with persistent Docker volume
- **Session**: Auto-saved in browser
- **Backups**: Manual backups recommended for production
- **Durability**: Survives container restarts

---

## 🔒 Security Features

✅ **JWT Authentication** - Token-based, not session-based  
✅ **Password Hashing** - Bcrypt with salt  
✅ **CORS Enabled** - Safe cross-origin requests  
✅ **Input Validation** - All inputs validated  
✅ **Auto Session Mgmt** - Secure token handling  

---

## 📱 Browser Support

| Browser | Support | Version |
|---------|---------|---------|
| Chrome | ✅ Full | Latest |
| Firefox | ✅ Full | Latest |
| Safari | ✅ Full | 14+ |
| Edge | ✅ Full | Latest |
| IE 11 | ❌ Not supported | - |

**Recommended**: Chrome or Firefox (latest)

---

## ✅ Status

- **Version**: 1.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-09-01
- **All Tests**: Passed ✓
- **Pre-seeded Data**: ✓ Included

---

## 📖 Quick Links

| Resource | Purpose |
|----------|---------|
| [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) | Setup steps |
| [USER_GUIDE.md](USER_GUIDE.md) | Dashboard guide |
| [API_REFERENCE.md](API_REFERENCE.md) | API documentation |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Cheat sheet |
| Swagger UI | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

**Ready to use! Access dashboard at http://localhost:8501** 🎉

**Questions? Read the documentation or check [USER_GUIDE.md](USER_GUIDE.md) → Troubleshooting**
