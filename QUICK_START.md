# Quick Start Guide - Full Stack Setup

## Complete Local Testing (API + Frontend)

### Prerequisites
You have everything installed already! ✅

---

## 🚀 Full Stack Demo (API + Frontend)

### **Terminal 1: Start MongoDB**

```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

Or if you have Homebrew MongoDB:
```bash
brew services start mongodb-community
```

Wait 5-10 seconds for MongoDB to fully start.

---

### **Terminal 2: Start FastAPI Backend**

```bash
cd "/Users/shubhamgodha/Documents/Github Repos/Antonia/NEW VERSION 2"
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

### **Terminal 3: Seed Database**

```bash
cd "/Users/shubhamgodha/Documents/Github Repos/Antonia/NEW VERSION 2"
source venv/bin/activate
python scripts/seed.py
```

You should see:
```
✅ Database seeding completed successfully
Database contains 3 authors and 5 books
```

---

### **Terminal 4: Start Streamlit Frontend**

```bash
cd "/Users/shubhamgodha/Documents/Github Repos/Antonia/NEW VERSION 2"
source venv/bin/activate
streamlit run frontend/app.py
```

You should see:
```
Local URL: http://localhost:8501
Network URL: http://192.168.1.102:8501
```

✅ **Frontend is now running!**

---

## 🌐 Access the Application

Open your browser:

| Component | URL | What You Can Do |
|-----------|-----|-----------------|
| **Streamlit UI** | http://localhost:8501 | Browse books, create, update, delete |
| **API Docs** | http://localhost:8000/docs | Test API endpoints interactively |
| **ReDoc** | http://localhost:8000/redoc | Alternative API documentation |
| **Health Check** | http://localhost:8000/health | Verify API is running |

---

## 📊 Frontend Features

### Navigation Menu (Left Sidebar)
1. **Books** - Browse, search, filter books
2. **Create Book** - Add new books
3. **Update Book** - Edit existing books
4. **Authors** - View authors and their books
5. **Publishers** - View publisher statistics

### Books Page
- ✅ Browse all books
- ✅ Search by title
- ✅ Filter by author ID
- ✅ View tags
- ✅ Pagination
- ✅ Edit/Delete buttons

### Create Book
- ✅ Form with validation
- ✅ Auto-validation
- ✅ Success message

### Update Book
- ✅ Select book by ID
- ✅ Edit any field
- ✅ Partial updates

### Authors
- ✅ List all authors
- ✅ Show book count per author
- ✅ View books by author

### Publishers
- ✅ Search by publisher name
- ✅ View average pages
- ✅ See total book count

---

## 🧪 Run Tests

### While services are running, in Terminal 5:

```bash
cd "/Users/shubhamgodha/Documents/Github Repos/Antonia/NEW VERSION 2"
source venv/bin/activate
pytest tests/integration/ -v
```

---

## 📝 Example Workflow

### 1. View Books (Streamlit)
- Go to http://localhost:8501
- Click "Books" in sidebar
- See the 5 seeded books

### 2. Create a Book (Streamlit)
- Click "Create Book"
- Fill in:
  - Book ID: 100
  - Title: "My Test Book"
  - Author ID: 1
  - Publisher: "Test Publisher"
  - Pages: 300
  - Tags: test, python
- Click "Create Book"
- Success message appears!

### 3. View in API (Browser)
- Go to http://localhost:8000/docs
- Click "GET /books"
- Click "Try it out"
- Scroll down - see your new book in the list!

### 4. Edit Book (Streamlit)
- Click "Update Book"
- Enter Book ID: 100
- Change title to "Updated Test Book"
- Click "Update Book"
- Success message!

### 5. Delete Book (Streamlit)
- Click "Books"
- Scroll to book ID 100
- Click "Delete"
- Confirm
- Book is gone!

---

## 🔧 Troubleshooting

### "Connection refused" on Streamlit
**Problem:** API not running
**Solution:** Start Terminal 2 with `uvicorn` command

### "Cannot connect to MongoDB"
**Problem:** MongoDB not running
**Solution:** Start MongoDB in Terminal 1

### "ModuleNotFoundError: No module named 'frontend'"
**Problem:** Import path issue (FIXED ✅)
**Solution:** Already fixed in the code

### Streamlit says "App stopped"
**Problem:** Usually API connection issue
**Solution:** Verify API is running on port 8000

### Port already in use
```bash
# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 8501
lsof -i :8501 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

---

## 📋 Checklist

- [ ] MongoDB running (Terminal 1)
- [ ] API server running (Terminal 2)
- [ ] Database seeded (Terminal 3)
- [ ] Streamlit running (Terminal 4)
- [ ] Can access http://localhost:8501
- [ ] Can see books in UI
- [ ] Can create/update/delete books

---

## 🎯 Next Steps

1. **Run the full stack** following the steps above
2. **Try creating a book** in the Streamlit UI
3. **Check the API docs** at http://localhost:8000/docs
4. **Run tests** to verify everything works

---

## 💡 Tips

- **Reload code**: Streamlit auto-reloads when you edit files
- **API docs**: The `/docs` endpoint has an interactive API explorer
- **Sample data**: Run `python scripts/seed.py` to repopulate with sample data
- **View logs**: Both API and Streamlit print logs in their terminals

---

**Everything is ready! Start Terminal 1 and follow the steps above.** 🚀
