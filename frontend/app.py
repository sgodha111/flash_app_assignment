"""Streamlit frontend for Book Catalog API with JWT Authentication."""

import logging
import sys
from pathlib import Path
import streamlit as st
import requests
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from frontend.api_client import get_client

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="📚 Book Library Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Function to get session file path
def get_session_file():
    session_dir = Path.home() / ".streamlit_sessions"
    session_dir.mkdir(exist_ok=True)
    return session_dir / "book_library_session.json"

# Function to load session from file
def load_session_from_file():
    session_file = get_session_file()
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                return session_data.get("auth_token"), session_data.get("user_email")
        except:
            return None, None
    return None, None

# Function to save session to file
def save_session_to_file(token, email):
    session_file = get_session_file()
    session_data = {
        "auth_token": token,
        "user_email": email,
        "login_time": datetime.now().isoformat()
    }
    with open(session_file, 'w') as f:
        json.dump(session_data, f)

# Function to clear session file
def clear_session_file():
    session_file = get_session_file()
    if session_file.exists():
        session_file.unlink()

# Initialize session state with defaults
if "auth_token" not in st.session_state:
    # Try to load from file first
    token, email = load_session_from_file()
    st.session_state.auth_token = token
    st.session_state.user_email = email
else:
    # Ensure we have both token and email
    if st.session_state.auth_token and "user_email" not in st.session_state:
        st.session_state.user_email = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "edit_book_id" not in st.session_state:
    st.session_state.edit_book_id = None

if "show_author_modal" not in st.session_state:
    st.session_state.show_author_modal = False

# Persist auth token using browser localStorage
st.markdown("""
    <script>
    // Save token to localStorage whenever session state changes
    function saveAuthToLocalStorage(token, email) {
        if (token) {
            localStorage.setItem('auth_token', token);
            localStorage.setItem('user_email', email);
            localStorage.setItem('login_time', new Date().toISOString());
        }
    }
    </script>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# LOGIN PAGE - Show if not authenticated
if not st.session_state.auth_token:
    st.markdown("""
        <div style='text-align: center; margin: 5rem 0;'>
            <h1>📚 Book Library Catalog</h1>
            <p style='font-size: 1.2rem; color: #666;'>Secure Login Required</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("### 🔐 Login")
        st.write("")

        email = st.text_input(
            "Email Address",
            placeholder="admin@example.com",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        st.write("")

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("🔓 Login", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("❌ Please enter both email and password")
                else:
                    try:
                        response = requests.post(
                            "http://api:8000/auth/login",
                            json={"email": email, "password": password},
                            timeout=5
                        )

                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.auth_token = data.get("access_token")
                            st.session_state.user_email = email

                            # Save session to file for persistence across page refreshes
                            save_session_to_file(st.session_state.auth_token, st.session_state.user_email)

                            # Also store in localStorage for client-side reference
                            st.markdown(f"""
                                <script>
                                localStorage.setItem('auth_token', '{st.session_state.auth_token}');
                                localStorage.setItem('user_email', '{st.session_state.user_email}');
                                localStorage.setItem('login_time', '{datetime.now().isoformat()}');
                                </script>
                                """, unsafe_allow_html=True)

                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                    except Exception as e:
                        st.error(f"❌ Connection error: {str(e)}")

        with col_btn2:
            if st.button("🔄 Reset", use_container_width=True):
                st.rerun()

        st.write("")
        st.divider()
        st.write("")

        st.markdown("### 👥 Demo Users")
        st.info("""
        **Admin User:**
        - Email: `admin@example.com`
        - Password: `admin@123`

        **Other Users:**
        - john@example.com / john@1234
        - jane@example.com / jane@1234
        - developer@example.com / dev@12345
        - demo@example.com / demo@1234
        """)

    st.stop()

try:
    client = get_client(token=st.session_state.auth_token)
    health = client.health()
except Exception as e:
    st.error(f"❌ Failed to connect to API: {e}")
    if st.button("🔄 Logout"):
        st.session_state.auth_token = None
        st.session_state.user_email = None
        clear_session_file()
        st.markdown("""
            <script>
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_email');
            localStorage.removeItem('login_time');
            </script>
            """, unsafe_allow_html=True)
        st.rerun()
    st.stop()

col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.markdown("""
        <div class="dashboard-header">
            <h1>📚 Book Catalog Dashboard</h1>
            <p>Manage your book collection with ease</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.write("")
    st.write("")
    user_col1, user_col2 = st.columns(2)

    with user_col1:
        st.caption(f"👤 {st.session_state.user_email}")

    with user_col2:
        if st.button("🚪 Logout", help="Logout from the application"):
            st.session_state.auth_token = None
            st.session_state.user_email = None
            clear_session_file()
            st.markdown("""
                <script>
                localStorage.removeItem('auth_token');
                localStorage.removeItem('user_email');
                localStorage.removeItem('login_time');
                </script>
                """, unsafe_allow_html=True)
            st.rerun()

with st.sidebar:
    st.markdown("# 🚀 Navigation")
    st.divider()

    page = st.radio(
        "Select Page",
        ["📖 Books", "✍️ Create Book", "👥 Authors", "🏢 Publishers", "📋 Info & Links"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("### 📊 Statistics")
    try:
        books_response = client.list_books(limit=1)
        authors_response = client.list_authors(limit=1)
        st.metric("Total Books", books_response.get("total", 0))
        st.metric("Total Authors", authors_response.get("total", 0))
    except:
        pass

def create_author_modal():
    st.write("### Add a New Author")

    col1, col2 = st.columns(2)
    with col1:
        author_id = st.number_input("Author ID", min_value=1, step=1, value=100, key="new_author_id_input")
        name = st.text_input("Name", key="new_author_name_input", placeholder="e.g., Stephen King")

    with col2:
        birth_date = st.date_input("Birth Date (optional)", key="new_author_birth_input")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Add Author", use_container_width=True, key="add_author_btn"):
            if not name or name.strip() == "":
                st.error("❌ Author name is required")
            else:
                try:
                    author_data = {
                        "id": int(author_id),
                        "name": name.strip(),
                    }
                    if birth_date:
                        author_data["birth_date"] = birth_date.isoformat()

                    response = client.create_author(author_data)
                    st.success(f"✅ Author '{name}' added successfully!")
                    st.rerun()
                except Exception as e:
                    error_str = str(e)
                    if "409" in error_str or "already exists" in error_str:
                        st.error(f"❌ Author ID {author_id} already exists. Please use a different ID.")
                    else:
                        st.error(f"❌ Failed to add author: {e}")

    with col2:
        if st.button("❌ Cancel", use_container_width=True, key="cancel_author_btn"):
            st.session_state.show_author_modal = False
            st.rerun()

if page == "📖 Books":
    # Check if edit modal should be shown
    if "edit_book_id" in st.session_state and st.session_state.edit_book_id:
        try:
            book = client.get_book(st.session_state.edit_book_id)

            st.markdown("### ✏️ Edit Book")

            col1, col2 = st.columns(2)

            with col1:
                edit_title = st.text_input("📖 Title", value=book.get('title', ''), key="edit_title_input")
                edit_author_id = st.number_input("👤 Author ID", value=book.get('author_id', 1), min_value=1, step=1, key="edit_author_input")
                edit_publisher = st.text_input("🏢 Publisher", value=book.get('publisher', ''), key="edit_publisher_input")

            with col2:
                edit_pages = st.number_input("📄 Pages", value=book.get('pages', 1), min_value=1, step=1, key="edit_pages_input")
                edit_tags = st.text_input("🏷️ Tags (comma-separated)", value=", ".join(book.get('tags', [])), key="edit_tags_input")

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                if st.button("✅ Save Changes", use_container_width=True, type="primary", key="save_edit_btn"):
                    if not all([edit_title, edit_author_id, edit_publisher, edit_pages]):
                        st.error("❌ Please fill in all required fields")
                    else:
                        try:
                            tags = [tag.strip() for tag in edit_tags.split(",") if tag.strip()]

                            book_update = {
                                "title": edit_title,
                                "author_id": int(edit_author_id),
                                "publisher": edit_publisher,
                                "pages": int(edit_pages),
                                "tags": tags if tags else []
                            }

                            response = client.update_book(st.session_state.edit_book_id, book_update)
                            st.success(f"✅ Book updated successfully!")
                            st.session_state.edit_book_id = None
                            st.rerun()

                        except Exception as e:
                            error_str = str(e)
                            if "422" in error_str:
                                st.error(f"❌ Author ID {edit_author_id} does not exist.")
                            else:
                                st.error(f"❌ Failed to update book: {e}")

            with col2:
                if st.button("❌ Cancel", use_container_width=True, key="cancel_edit_btn"):
                    st.session_state.edit_book_id = None
                    st.rerun()

            st.divider()

        except Exception as e:
            st.error(f"❌ Failed to load book for editing: {e}")
            if st.button("❌ Close", key="close_edit_error_btn"):
                st.session_state.edit_book_id = None
                st.rerun()
    else:
        # Show book library
        st.header("📖 Book Library")

        col1, col2, col3 = st.columns(3)
        with col1:
            search_title = st.text_input("🔍 Search by title", key="search_title")
        with col2:
            search_author = st.number_input("👤 Filter by author ID", value=0, min_value=0, step=1)
        with col3:
            page_num = st.number_input("📄 Page", value=1, min_value=1, step=1)

        st.divider()

        try:
            response = client.list_books(
                page=page_num,
                limit=10,
                title=search_title if search_title else None,
                author_id=search_author if search_author > 0 else None,
            )

            total = response.get("total", 0)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Books", total)
            with col2:
                st.metric("Page", page_num)
            with col3:
                st.metric("Per Page", 10)

            st.divider()

            books = response.get("items", [])
            if books:
                for book in books:
                    with st.container(border=True):
                        col1, col2, col3 = st.columns([3, 1, 1])

                        with col1:
                            st.markdown(f"### 📖 {book['title']}")
                            st.write(f"**Author ID:** {book['author_id']}")
                            st.write(f"**Publisher:** {book['publisher']}")
                            st.write(f"**Pages:** {book['pages']}")
                            if book.get('tags'):
                                tags_str = " | ".join([f"`{tag}`" for tag in book['tags']])
                                st.write(f"**Tags:** {tags_str}")
                            st.write(f"🆔 **Book ID:** {book['id']}")

                        with col2:
                            if st.button("✏️ Edit", key=f"edit_{book['id']}", use_container_width=True):
                                st.session_state.edit_book_id = book['id']
                                st.rerun()

                        with col3:
                            if st.button("🗑️ Delete", key=f"delete_{book['id']}", use_container_width=True):
                                try:
                                    client.delete_book(book['id'])
                                    st.success(f"✅ Book {book['id']} deleted!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Failed to delete: {e}")
            else:
                st.info("📭 No books found")

        except Exception as e:
            st.error(f"❌ Error loading books: {e}")

elif page == "✍️ Create Book":
    # Initialize form state
    if "create_title" not in st.session_state:
        st.session_state.create_title = ""
    if "create_publisher" not in st.session_state:
        st.session_state.create_publisher = ""
    if "create_tags" not in st.session_state:
        st.session_state.create_tags = ""
    if "create_pages" not in st.session_state:
        st.session_state.create_pages = 1

    # Success modal
    if "show_success_modal" in st.session_state and st.session_state.show_success_modal:
        st.success(f"✅ Book '{st.session_state.success_book_title}' created successfully with ID {st.session_state.success_book_id}!")
        st.info("📋 Form cleared. Ready to create another book.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Great! Create Another", use_container_width=True, type="primary", key="continue_create_btn"):
                st.session_state.show_success_modal = False
                st.session_state.create_title = ""
                st.session_state.create_publisher = ""
                st.session_state.create_tags = ""
                st.session_state.create_pages = 1
                st.rerun()
        with col2:
            if st.button("📖 Go to Books", use_container_width=True, key="go_to_books_btn"):
                st.session_state.show_success_modal = False
                st.rerun()

        st.stop()

    st.header("✍️ Create New Book")

    try:
        next_id_response = requests.get(
            "http://api:8000/books/next-id",
            headers={"Authorization": f"Bearer {st.session_state.auth_token}"},
            timeout=5
        )

        if next_id_response.status_code == 200:
            next_id = next_id_response.json().get("next_id", 1)
            st.info(f"📌 Next Book ID: **{next_id}** (auto-generated)")
        else:
            next_id = 1
    except:
        next_id = 1

    st.divider()

    try:
        authors_response = client.list_authors(limit=100)
        authors_list = authors_response.get("items", [])

        if authors_list:
            authors_dict = {f"{a['name']} (ID: {a['id']})": a['id'] for a in authors_list}
            has_authors = True
        else:
            authors_dict = {}
            has_authors = False
    except Exception as e:
        authors_dict = {}
        has_authors = False

    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("📖 Title", placeholder="Book title", value=st.session_state.create_title)
        st.session_state.create_title = title

        if has_authors and authors_dict:
            author_name = st.selectbox("👤 Author", list(authors_dict.keys()))
            author_id = authors_dict[author_name]
        else:
            st.error("❌ No authors available. Please add authors first in the Authors tab.")
            author_id = 0

        publisher = st.text_input("🏢 Publisher", placeholder="Publisher name", value=st.session_state.create_publisher)
        st.session_state.create_publisher = publisher

    with col2:
        pages = st.number_input("📄 Pages", min_value=1, step=1, value=st.session_state.create_pages)
        st.session_state.create_pages = pages
        tags_input = st.text_input("🏷️ Tags (comma-separated)", placeholder="e.g., Python, Development", value=st.session_state.create_tags)
        st.session_state.create_tags = tags_input

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Create Book", use_container_width=True, type="primary", key="create_book_btn"):
            if not all([title, author_id, publisher, pages]):
                st.error("❌ Please fill in all required fields")
            else:
                try:
                    try:
                        existing_books = client.list_books(limit=100)
                        existing_titles = [b['title'].lower() for b in existing_books.get("items", [])]

                        if title.lower() in existing_titles:
                            st.error(f"❌ Book title '{title}' already exists. Please use a different title.")
                            st.stop()
                    except:
                        pass

                    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

                    book_data = {
                        "id": next_id,
                        "title": title,
                        "author_id": int(author_id),
                        "publisher": publisher,
                        "pages": int(pages),
                        "tags": tags if tags else []
                    }

                    response = client.create_book(book_data)

                    # Store success info and show modal
                    st.session_state.show_success_modal = True
                    st.session_state.success_book_title = title
                    st.session_state.success_book_id = next_id

                    # Clear form fields
                    st.session_state.create_title = ""
                    st.session_state.create_publisher = ""
                    st.session_state.create_tags = ""
                    st.session_state.create_pages = 1

                    st.rerun()

                except Exception as e:
                    error_str = str(e)
                    if "409" in error_str:
                        st.error(f"❌ Book ID {next_id} already exists. Please refresh the page.")
                    elif "422" in error_str:
                        st.error(f"❌ Author does not exist. Please add the author first.")
                    else:
                        st.error(f"❌ Failed to create book: {e}")

    with col2:
        if st.button("🔄 Reset Form", use_container_width=True, key="reset_form_btn"):
            # Clear all form fields
            st.session_state.create_title = ""
            st.session_state.create_publisher = ""
            st.session_state.create_tags = ""
            st.session_state.create_pages = 1
            st.rerun()

elif page == "👥 Authors":
    st.header("👥 Authors")

    col1, col2 = st.columns([3, 1])

    with col2:
        if st.button("➕ Add New Author", use_container_width=True, key="add_author_modal_btn"):
            st.session_state.show_author_modal = True

    st.divider()

    if st.session_state.get("show_author_modal", False):
        create_author_modal()
        st.divider()

    try:
        response = client.list_authors(limit=100)
        authors = response.get("items", [])

        if authors:
            for author in authors:
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(f"### 👤 {author['name']}")
                        st.write(f"**ID:** {author['id']}")
                        st.write(f"**Books Written:** {author.get('book_count', 0)}")

                    with col2:
                        if st.button("📖 View Books", key=f"author_books_{author['id']}", use_container_width=True):
                            try:
                                books_response = client.get_author_books(author['id'])
                                books = books_response.get("items", [])
                                if books:
                                    st.write("**Books by this author:**")
                                    for book in books:
                                        st.write(f"- {book['title']}")
                                else:
                                    st.info("No books by this author")
                            except Exception as e:
                                st.error(f"❌ Failed to load books: {e}")
        else:
            st.info("📭 No authors found")

    except Exception as e:
        st.error(f"❌ Error loading authors: {e}")

elif page == "🏢 Publishers":
    st.header("🏢 Publishers Analytics")

    try:
        books_response = client.list_books(limit=100)
        all_books = books_response.get("items", [])

        if all_books:
            publisher_names = sorted(list(set([b.get('publisher', 'Unknown') for b in all_books if b.get('publisher')])))
        else:
            publisher_names = []
    except Exception as e:
        st.error(f"❌ Error fetching books: {e}")
        publisher_names = []

    if publisher_names:
        publisher_name = st.selectbox(
            "🏢 Select Publisher",
            publisher_names,
            key="publisher_select_input"
        )

        st.divider()

        if publisher_name:
            try:
                response = client.get_publisher_stats(publisher_name)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Average Pages", f"{response.get('average_pages', 0):.0f}")
                with col2:
                    st.metric("Total Books", response.get('book_count', 0))

                st.divider()
                st.markdown("### 📚 Books by this Publisher")

                if all_books:
                    publisher_books = [b for b in all_books if b.get('publisher') == publisher_name]

                    if publisher_books:
                        for book in publisher_books:
                            st.write(f"- **{book['title']}** (Pages: {book['pages']})")
                    else:
                        st.info("No books found for this publisher")

            except Exception as e:
                st.error(f"❌ Publisher not found or error: {e}")
    else:
        st.info("📭 No publishers found in the system. Create some books first.")

elif page == "📋 Info & Links":
    st.header("📋 Information & Links")

    st.markdown("### 🔗 Quick Links")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("[🌐 **API Documentation (Swagger)**](http://localhost:8000/docs)")

    with col2:
        st.markdown("[📚 **ReDoc (API Reference)**](http://localhost:8000/redoc)")

    with col3:
        if st.button("💚 Health Check", use_container_width=True, key="health_check_btn"):
            try:
                health = requests.get("http://api:8000/health", timeout=5).json()
                st.success(f"✅ API Status: {health.get('status', 'healthy')}")
            except:
                st.error("❌ API is not responding")

    st.divider()

    st.markdown("### 📚 About This Application")
    st.info("""
    **Book Library API**

    A production-ready REST API for managing books and authors built with:
    - **Backend:** FastAPI with JWT Authentication
    - **Database:** MongoDB
    - **Frontend:** Streamlit
    - **Infrastructure:** Docker & Docker Compose

    **Features:**
    - 📖 Complete CRUD operations
    - 👤 Author management
    - 🏢 Publisher analytics
    - 🔐 JWT-based authentication
    - 🔍 Advanced filtering and search
    """)

    st.divider()

    st.markdown("### 👨‍💻 Developer Information")
    st.info(f"""
    **Current User:** {st.session_state.user_email}

    **API Base URL:** http://api:8000
    **Frontend:** http://localhost:8501
    **API Documentation:** http://localhost:8000/docs
    **ReDoc:** http://localhost:8000/redoc
    """)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔗 Direct Links")
        st.markdown("""
        - [📖 Swagger UI](http://localhost:8000/docs)
        - [📚 ReDoc](http://localhost:8000/redoc)
        - [💚 Health Check](http://localhost:8000/health)
        """)

    with col2:
        st.markdown("### 📖 Quick Reference")
        st.markdown("""
        **Test Credentials:**
        - Email: admin@example.com
        - Password: admin@123

        **Base URL:** http://api:8000

        **Session Duration:** 24 hours
        """)
