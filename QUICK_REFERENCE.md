# 📚 Quick Reference Card

## 🔐 Login
**Email**: admin@example.com  
**Password**: admin@123

Other users: john@, jane@, developer@, demo@ → passwords: john@1234, jane@1234, dev@12345, demo@1234

---

## 🗺️ Pages (Dashboard)

| Page | Icon | Quick Action |
|------|------|--------------|
| Books | 📖 | Search/filter books, paginate |
| Create Book | ✍️ | Add new book (author required) |
| Authors | 👥 | Add author or view their books |
| Publishers | 🏢 | Select publisher, view stats |
| Info & Links | 📋 | Access API docs & health check |

---

## ⚡ Quick Actions

**Search Books**: Books page → Type title → Results update  
**Filter by Author**: Books page → Enter author ID  
**Add Author**: Authors page → + Add New Author → Enter ID & Name  
**Create Book**: Create Book page → Fill form → Select author (required) → Submit  
**View Author's Books**: Authors page → Click 📖 View Books  
**Publisher Stats**: Publishers page → Select publisher → View metrics  

---

## 🔗 URLs

| Resource | URL |
|----------|-----|
| Dashboard | http://localhost:8501 |
| API | http://localhost:8000 |
| Swagger (API test) | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

## 🚨 Quick Fixes

| Problem | Fix |
|---------|-----|
| Author missing | Create on Authors page first |
| Author ID exists | Use different unique ID |
| No books showing | Create book on Create Book page |
| Login fails | Check email/password (case-sensitive) |
| Page frozen | Refresh (Ctrl+R) or check http://localhost:8000/health |
| "Connection error" | Check API: http://localhost:8000/health |

---

## 🐳 Docker Commands

| Task | Command |
|------|---------|
| Start | `docker-compose up -d` |
| Stop | `docker-compose down` |
| Logs | `docker-compose logs` |
| Status | `docker-compose ps` |
| Restart | `docker-compose restart` |
| Clean | `docker-compose down -v` |

---

## 5️⃣-Minute Setup

1. Login (30 sec)
2. Add Author (30 sec)
3. Create Book (1 min)
4. Search Result (1 min)
5. Check Stats (1 min)

---

## 🔐 Security

✅ JWT auth (24hr expiry)  
✅ Passwords hashed  
✅ Session auto-saves  
✅ Logout clears data  

---

## 📚 Full Docs

| Need | File | Time |
|------|------|------|
| Overview | README.md | 5 min |
| Dashboard | USER_GUIDE.md | 15 min |
| API | API_REFERENCE.md | 10 min |
| Setup | INSTALLATION_GUIDE.md | 5 min |

---

**Keep this page bookmarked! 📌**
