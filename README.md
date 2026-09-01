# 📚 Book Library - Complete Documentation

A production-ready REST API and web dashboard for managing books, authors, and publishers.

**Built with**: FastAPI • MongoDB • Streamlit • Docker

---

## 🚀 Quick Start

### Launch Application
```bash
docker-compose up -d
```

### Access Points
| Service | URL |
|---------|-----|
| **Dashboard** | http://localhost:8501 |
| **API Swagger** | http://localhost:8000/docs |
| **API Redoc** | http://localhost:8000/redoc |
| **API Health** | http://localhost:8000/health |

### Login
```
Email: admin@example.com
Password: admin@123
```

---

## 📖 Documentation

This project includes comprehensive documentation:

### For Users
**→ See [USER_GUIDE.md](USER_GUIDE.md)** - Complete dashboard guide
- All 5 pages explained
- Step-by-step workflows
- Troubleshooting guide
- Screenshots and examples

### For Quick Lookup
**→ See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - One-page reference card
- Login credentials
- Page navigation
- Common tasks
- Quick fixes

### For Developers/API
**→ See [API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
- All 13 endpoints
- Request/response formats
- Authentication details
- Testing with Swagger

---

## 🏗️ Architecture

```
┌─────────────────────┐
│  Streamlit Frontend │ (Port 8501)
└──────────┬──────────┘
           │ HTTP
           ↓
┌─────────────────────┐
│  FastAPI Backend    │ (Port 8000)
└──────────┬──────────┘
           │ MongoDB Driver
           ↓
┌─────────────────────┐
│  MongoDB Database   │ (Port 27017)
└─────────────────────┘
```

---

## 📋 Dashboard Features

### 5 Main Pages

| Page | Purpose |
|------|---------|
| **📖 Books** | Search, filter, and browse books |
| **✍️ Create Book** | Add new books to library |
| **👥 Authors** | Manage authors |
| **🏢 Publishers** | View publisher statistics |
| **📋 Info & Links** | Access API documentation |

---

## 🔐 Authentication

- **JWT tokens** with 24-hour expiry
- **Bcrypt password** hashing
- **5 demo users** included
- Auto-session persistence

### Demo Credentials
```
admin@example.com       / admin@123
john@example.com        / john@1234
jane@example.com        / jane@1234
developer@example.com   / dev@12345
demo@example.com        / demo@1234
```

---

## 🗄️ Database

**MongoDB** with persistent volumes:
- Books collection
- Authors collection
- Users collection
- Automatic backups via volumes

---

## 📡 API Overview

**13 Total Endpoints**:
- 6 Books endpoints
- 4 Authors endpoints
- 1 Publishers endpoint
- 2 Health/Status endpoints

→ See [API_REFERENCE.md](API_REFERENCE.md) for complete details

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI 0.100+ |
| **Database** | MongoDB 7.0 |
| **Frontend** | Streamlit 1.28+ |
| **Container** | Docker & Docker Compose |
| **Auth** | JWT + Bcrypt |
| **Async** | Motor (async MongoDB) |

---

## 📁 Project Structure

```
.
├── README.md                    ← Project overview (this file)
├── USER_GUIDE.md               ← Dashboard user guide
├── QUICK_REFERENCE.md          ← Quick lookup card
├── API_REFERENCE.md            ← API documentation
├── docker-compose.yml          ← Container configuration
├── Dockerfile                  ← API container
├── Dockerfile.frontend         ← Frontend container
│
├── app/                        ← Backend (FastAPI)
│   ├── main.py
│   ├── config.py
│   ├── database/
│   ├── api/routes/
│   ├── schemas/
│   └── services/
│
├── frontend/                   ← Frontend (Streamlit)
│   └── app.py
│
└── scripts/                    ← Utilities
    └── seed_users.py
```

---

## 🚀 Getting Started (5 Minutes)

### Step 1: Start Application
```bash
docker-compose up -d
```

### Step 2: Access Dashboard
Go to http://localhost:8501

### Step 3: Login
```
Email: admin@example.com
Password: admin@123
```

### Step 4: Explore
- Browse the Books page (empty initially)
- Go to Authors → Add Author
- Go to Create Book → Add Book
- Go to Publishers → View Statistics

→ Full guide: [USER_GUIDE.md](USER_GUIDE.md)

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| **README.md** | Project overview | 5 min |
| **USER_GUIDE.md** | Complete dashboard guide | 15 min |
| **QUICK_REFERENCE.md** | One-page quick lookup | 2 min |
| **API_REFERENCE.md** | API endpoints & testing | 10 min |

---

## 🔍 Feature Highlights

✅ **Full CRUD Operations** - Create, read, update, delete books
✅ **Advanced Search** - Real-time title search
✅ **Filtering** - Filter books by author
✅ **Pagination** - Browse large datasets
✅ **Analytics** - Publisher statistics and metrics
✅ **JWT Security** - Token-based authentication
✅ **Auto-Seeding** - Demo data included
✅ **Docker Ready** - One-command deployment
✅ **Responsive** - Works on desktop/tablet
✅ **API Testing** - Swagger UI built-in

---

## 🆘 Support & Troubleshooting

### Common Issues

**"Connection error" when creating book**
→ Check API is running: http://localhost:8000/health

**Author not in dropdown**
→ Create author first (Authors page)

**No books showing**
→ Add books via Create Book page

**Login fails**
→ Check email/password spelling (case-sensitive)

→ Full troubleshooting: [USER_GUIDE.md](USER_GUIDE.md)

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| Dashboard | http://localhost:8501 |
| API Swagger | http://localhost:8000/docs |
| API Redoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## 📝 Example Workflow

```
1. Login (admin@example.com / admin@123)
2. Add Author: Authors page → + Add New Author
3. Create Book: Create Book page → Fill form
4. View Result: Books page → See new book
5. Check Stats: Publishers page → Select publisher
```

---

## ✅ Pre-Submission Checklist

- [x] Dashboard fully functional
- [x] All 5 pages working
- [x] Login authentication working
- [x] Database seeded with demo data
- [x] API endpoints tested
- [x] Documentation complete
- [x] No duplication in docs
- [x] Clean and organized

---

## 📞 Getting Help

1. **For dashboard usage** → Read [USER_GUIDE.md](USER_GUIDE.md)
2. **For quick lookup** → See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
3. **For API details** → Check [API_REFERENCE.md](API_REFERENCE.md)
4. **For API testing** → Use Swagger at http://localhost:8000/docs
5. **For status check** → Run health check

---

## 📊 Version

- **Version**: 1.0.0
- **Status**: Production Ready
- **Last Updated**: 2026-09-01

---

**Start with README.md (this file), then pick your documentation:**
- 👤 **Dashboard user?** → [USER_GUIDE.md](USER_GUIDE.md)
- ⚡ **Need quick answer?** → [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 👨‍💻 **Developer/API?** → [API_REFERENCE.md](API_REFERENCE.md)

---

**Ready to use! Access dashboard at http://localhost:8501 🚀**
