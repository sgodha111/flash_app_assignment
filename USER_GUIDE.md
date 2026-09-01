# 📚 Book Library Dashboard - User Guide

Complete guide to using the Book Library Dashboard.

---

## 🔐 Login

**Dashboard**: http://localhost:8501

**Demo Credentials**:
```
Email: admin@example.com
Password: admin@123

Other users: john@, jane@, developer@, demo@ (all @example.com)
Passwords: john@1234, jane@1234, dev@12345, demo@1234
```

**Login Steps**:
1. Enter email
2. Enter password
3. Click **🔓 Login**

---

## 📊 Dashboard Layout

**Left Sidebar**:
- Navigation menu (5 pages)
- Total Books count
- Total Authors count
- Logout button

**Pages**:
- 📖 **Books** - Search & browse
- ✍️ **Create Book** - Add new
- 👥 **Authors** - Manage
- 🏢 **Publishers** - Statistics
- 📋 **Info & Links** - Resources

---

## 📖 Books Page

**Search for books**:
1. Enter title in search field
2. Results update instantly
3. Combine with author filter for precision

**Filter by Author**:
1. Enter author ID number
2. Use +/- buttons to adjust
3. Shows only that author's books

**Pagination**:
- Navigate between pages
- Adjust items per page
- See total book count

---

## ✍️ Create Book Page

**Required Fields**:
| Field | Example |
|-------|---------|
| Title | Harry Potter |
| Pages | 309 |
| Author | Select from dropdown |
| Publisher | Bloomsbury |

**Optional**: Tags (comma-separated)

**Important**: ⚠️ **Author must exist first!**

**Steps**:
1. Enter title
2. Enter pages
3. Select author from dropdown
4. Add tags (optional)
5. Enter publisher
6. Click **✨ Create Book**

---

## 👥 Authors Page

**Add Author**:
1. Click **+ Add New Author**
2. Enter unique **Author ID**
3. Enter **Name**
4. Optionally add **Birth Date**
5. Click **✅ Add Author**

**View Author's Books**:
- Click **📖 View Books** on author card
- See all books by that author

---

## 🏢 Publishers Page

**View Statistics**:
1. Select publisher from dropdown
2. Auto-updates to show:
   - **Average Pages** - Mean pages per book
   - **Total Books** - Number of books
   - **Books List** - All books by publisher

---

## 📋 Info & Links Page

**Quick Resources**:
- 🔗 **Swagger UI** - Test API endpoints
- 📖 **Redoc** - API documentation
- ✅ **Health Check** - Verify API status

---

## 🔄 Complete Workflow: Add Your First Book

```
1. LOGIN
   └─ admin@example.com / admin@123

2. CREATE AUTHOR
   └─ 👥 Authors → + Add New Author
   └─ ID: 100, Name: Your Author Name
   └─ Click ✅ Add Author

3. CREATE BOOK
   └─ ✍️ Create Book
   └─ Title: Your Book Title
   └─ Pages: 300
   └─ Select: Your Author
   └─ Tags: Your, Tags (optional)
   └─ Publisher: Your Publisher
   └─ Click ✨ Create Book

4. VIEW BOOK
   └─ 📖 Books
   └─ Search: Your book title
   └─ See it in list

5. VIEW STATS
   └─ 🏢 Publishers
   └─ Select: Your Publisher
   └─ See statistics
```

---

## ❌ Troubleshooting

### Login Issues

**"Invalid email or password"**
- Check email spelling
- Verify password (case-sensitive)
- Try: admin@example.com / admin@123

**Login page keeps showing**
- Check API: http://localhost:8000/health
- Refresh page (Ctrl+R)
- Clear browser cache
- Restart browser

### Data Issues

**"No books found"**
- Create books via ✍️ Create Book page
- Need author first (go to Authors)

**Author not in dropdown**
- Go to 👥 Authors → + Add New Author
- Create the author
- Return to Create Book

**"Author ID already exists"**
- Use different ID number
- Check existing authors first

### Display Issues

**Page shows old data**
- Refresh page (Ctrl+R)
- Clear cache (Ctrl+Shift+Del)
- Logout and login again

**Buttons not responding**
- Wait for page to load
- Refresh page
- Check API health: http://localhost:8000/health

### API Issues

**"Connection error" when creating book**
- Check API running: http://localhost:8000/health
- Restart: `docker-compose restart api`
- View logs: `docker-compose logs api`

---

## 🔒 Session & Security

- ✅ **JWT Authentication** - Token-based secure login
- ✅ **Passwords Hashed** - Bcrypt encryption
- ✅ **Session Auto-Saves** - Persists across refreshes
- 🔄 **Token Expiry** - 24 hours
- 🚪 **Logout** - Clears all session data

---

## 💡 Tips

**For faster searches**: Use specific search terms + author filter

**For better performance**: Use modern browser (Chrome/Firefox), disable extensions, clear cache regularly

**Multiple users**: Each user has independent session

**Data backup**: Manually backup MongoDB volume if needed

---

## ❓ FAQ

| Q | A |
|---|---|
| Can I create books without authors? | No, author must exist first |
| How long is session active? | 24 hours (JWT token expiry) |
| Can multiple users login? | Yes, each has separate session |
| Can I edit books? | Yes, via Books page |
| Can I delete books? | Yes, use Books page |
| Is data backed up? | Data in MongoDB volume, manual backup recommended |
| What if API is slow? | Check health, restart containers |

---

## 📱 Browser Support

✅ Chrome (latest)  
✅ Firefox (latest)  
✅ Safari (macOS)  
✅ Edge (latest)

**Recommended**: Chrome or Firefox

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| Dashboard | http://localhost:8501 |
| API Swagger | http://localhost:8000/docs |
| API Health | http://localhost:8000/health |
| API Redoc | http://localhost:8000/redoc |

---

**For API development** → See [API_REFERENCE.md](API_REFERENCE.md)

**For quick lookup** → See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**For setup** → See [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

**Happy managing! 📚**
