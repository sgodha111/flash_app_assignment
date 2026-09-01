# 📚 Book Library Dashboard - User Guide

Complete guide to using the Book Library Dashboard application.

---

## Table of Contents

1. [Login](#login)
2. [Dashboard Overview](#dashboard-overview)
3. [Pages Guide](#pages-guide)
4. [Workflows](#workflows)
5. [Troubleshooting](#troubleshooting)

---

## Login

### Access Dashboard
Go to: **http://localhost:8501**

### Demo Credentials
```
Email: admin@example.com
Password: admin@123

Other users:
john@example.com / john@1234
jane@example.com / jane@1234
developer@example.com / dev@12345
demo@example.com / demo@1234
```

### Login Steps
1. Open dashboard URL
2. Enter email address
3. Enter password
4. Click **🔓 Login**
5. Redirected to dashboard

---

## Dashboard Overview

### Layout
```
┌─────────────────────────┐
│   Book Library Catalog  │
├──────────────┬──────────┤
│              │          │
│  Sidebar     │  Content │
│  Navigation  │  Area    │
│  & Stats     │          │
│              │          │
└──────────────┴──────────┘
```

### Left Sidebar
**Navigation**:
- 📖 Books
- ✍️ Create Book
- 👥 Authors
- 🏢 Publishers
- 📋 Info & Links

**Statistics**:
- Total Books count
- Total Authors count

### Top Right
- User email display
- 🚪 Logout button

---

## Pages Guide

### 📖 Books Page
**Purpose**: Browse and manage all books

**Features**:
- 🔍 Search by title (real-time)
- 🎯 Filter by author ID
- 📄 Pagination controls
- 📊 Display statistics

**How to Use**:
```
1. Enter book title in search → Results update instantly
2. Enter author ID in filter → Shows only that author's books
3. Click page numbers → Navigate results
4. Adjust "Per Page" → Change display count
```

**Example**:
```
Search: "Harry"
Filter: 1 (author ID)
Result: Harry Potter by author 1
```

---

### ✍️ Create Book Page
**Purpose**: Add new books to library

**Required Fields**:
| Field | Input | Example |
|-------|-------|---------|
| Title | Text | Harry Potter |
| Pages | Number | 309 |
| Author | Dropdown | Select from list |
| Publisher | Text | Bloomsbury |

**Optional Fields**:
| Field | Input |
|-------|-------|
| Tags | Comma-separated | Fantasy, Magic, Wizards |

**Steps**:
1. Enter book title
2. Enter page count
3. **Select author** (must exist!)
4. Add tags (optional)
5. Enter publisher name
6. Click **✨ Create Book**

**Important**:
⚠️ **Author must exist first!**
- If author missing: Go to Authors page → Add Author

**Example Workflow**:
```
Title: Harry Potter
Pages: 309
Author: J.K. Rowling (select from dropdown)
Tags: Fantasy, Magic, Wizards
Publisher: Bloomsbury
Result: ✅ Book created successfully
```

---

### 👥 Authors Page
**Purpose**: Manage book authors

**Features**:
- ➕ Add new authors
- 👁️ View author cards
- 📚 See books per author
- 📖 View author's books

**Author Card Shows**:
- Author name
- Author ID
- Books written count
- View Books button

**Add Author Steps**:
1. Click **+ Add New Author** button
2. Modal form appears
3. Enter **Author ID** (must be unique)
4. Enter **Name** (full name)
5. Optionally add **Birth Date**
6. Click **✅ Add Author**

**Example**:
```
ID: 100
Name: J.K. Rowling
Birth Date: 1965-07-31 (optional)
Result: ✅ Author added
```

---

### 🏢 Publishers Page
**Purpose**: View publisher analytics and statistics

**Features**:
- Publisher selector dropdown
- Average Pages metric
- Total Books count
- Books by publisher list

**How to Use**:
1. Click "Select Publisher" dropdown
2. Choose a publisher
3. View automatically updates:
   - Average Pages: Mean pages per book
   - Total Books: Number of books
   - Books List: All books published

**Example**:
```
Select: Bloomsbury
Average Pages: 320
Total Books: 5
Books:
- Harry Potter (pages)
- Other titles...
```

---

### 📋 Info & Links Page
**Purpose**: Access documentation and resources

**Quick Links**:
| Link | Purpose |
|------|---------|
| 🔗 API Documentation (Swagger) | Test API endpoints |
| 📖 Redoc | API reference |
| ✅ Health Check | Check API status |

**Technology Stack**:
- Backend: FastAPI with JWT
- Database: MongoDB
- Frontend: Streamlit
- Deploy: Docker Compose

---

## Workflows

### Complete Workflow: Add Book

```
STEP 1: LOGIN
└─ Email: admin@example.com
└─ Password: admin@123

STEP 2: CREATE AUTHOR
└─ Go to: 👥 Authors
└─ Click: + Add New Author
└─ Fill: ID: 10, Name: Your Author
└─ Result: ✅ Author added

STEP 3: CREATE BOOK
└─ Go to: ✍️ Create Book
└─ Fill: Title, Pages, Select Author
└─ Fill: Tags, Publisher
└─ Click: ✨ Create Book
└─ Result: ✅ Book created

STEP 4: VIEW BOOK
└─ Go to: 📖 Books
└─ Search: Your book title
└─ Result: See new book in list

STEP 5: VIEW STATS
└─ Go to: 🏢 Publishers
└─ Select: Your publisher
└─ Result: See statistics
```

### Quick Task: Search for Book

```
1. Go to 📖 Books page
2. Type title in search
3. Results update instantly
4. Optional: Filter by author ID
```

### Quick Task: View Author's Books

```
1. Go to 👥 Authors page
2. Find author card
3. Click 📖 View Books
4. See all books by author
```

---

## Troubleshooting

### Login Issues

**Problem**: "Invalid email or password"
```
Cause: Incorrect credentials
Fix:
1. Check email spelling
2. Verify password (case-sensitive)
3. Ensure Caps Lock is OFF
4. Try demo account: admin@example.com / admin@123
```

**Problem**: Login page keeps showing
```
Cause: Session issue or API unreachable
Fix:
1. Check API health: http://localhost:8000/health
2. Refresh page (Ctrl+R)
3. Clear browser cache
4. Restart browser
```

---

### Data Issues

**Problem**: "No books found" message
```
Cause: Database is empty
Fix:
1. Go to ✍️ Create Book page
2. Add books (need author first)
3. Refresh page
```

**Problem**: Author not in dropdown
```
Cause: Author hasn't been created
Fix:
1. Go to 👥 Authors page
2. Click + Add New Author
3. Create author first
4. Return to Create Book
```

**Problem**: "Author ID already exists" error
```
Cause: ID is not unique
Fix:
1. Use different ID number
2. Check existing authors first
3. Pick ID number not used
```

---

### Display Issues

**Problem**: Page shows old data
```
Cause: Browser cache or stale session
Fix:
1. Refresh page (Ctrl+R or Cmd+R)
2. Clear cache (Ctrl+Shift+Del)
3. Logout and login again
```

**Problem**: Buttons not responding
```
Cause: Page still loading or connection issue
Fix:
1. Wait for page to fully load
2. Refresh page
3. Check API health check
4. Verify internet connection
```

### API Connection Issues

**Problem**: "Connection error" when creating/updating
```
Cause: API server not running
Fix:
1. Check if API is running: http://localhost:8000/health
2. Restart containers: docker-compose restart
3. View logs: docker-compose logs api
```

---

## Security

### Your Session
- ✅ Auto-saves across page refreshes
- 🔄 Token expires: 24 hours
- 🚪 Logout clears all data
- 🔐 Passwords hashed with bcrypt

### Data Protection
- JWT token-based authentication
- All passwords hashed
- Secure API connections
- Input validation on all fields

---

## Browser Support

**Supported**:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (macOS)
- ✅ Edge (latest)

**Recommended**: Chrome or Firefox

---

## Performance Tips

### For Faster Searches
- Use specific search terms
- Combine search + filter
- Adjust items per page to smaller number

### For Better Experience
- Use modern browser (updated)
- Disable unnecessary extensions
- Clear cache periodically
- Keep sufficient RAM available

---

## FAQ

**Q: Can I create books without authors?**
A: No, author must exist first. Go to Authors page to create.

**Q: How long is my session active?**
A: Access token expires after 24 hours. Re-login needed.

**Q: Can multiple users login simultaneously?**
A: Yes, each user has independent session.

**Q: Is data backed up?**
A: Data persists in MongoDB volumes. Manual backups recommended.

**Q: Can I edit books after creating?**
A: Yes, books can be updated via Books page.

**Q: What if API is slow?**
A: Check API health. Restart containers if needed.

---

## Quick Links

| Resource | URL |
|----------|-----|
| Dashboard | http://localhost:8501 |
| API Swagger | http://localhost:8000/docs |
| API Redoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## 5-Minute Quick Start

1. **Login** (1 min) - admin@example.com / admin@123
2. **Add Author** (1 min) - Authors page → Add Author
3. **Create Book** (1.5 min) - Create Book page → Fill form
4. **View Book** (0.5 min) - Books page → Search
5. **Check Stats** (1 min) - Publishers page → Select publisher

---

## Getting Help

1. **For quick answers** → See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **For API details** → See [API_REFERENCE.md](API_REFERENCE.md)
3. **For API testing** → Visit Swagger at http://localhost:8000/docs
4. **For status** → Run health check

---

**Next**: See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for quick lookup or [README.md](README.md) for overview.

**Happy managing! 📚**
