"""Streamlit frontend for Antonie Book Catalog API - Professional Dashboard."""

import logging
from datetime import date
from typing import Optional
import sys
import streamlit as st
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from frontend.api_client import get_client

logger = logging.getLogger(__name__)

# Configure Streamlit page with modern design
st.set_page_config(
    page_title="📚 Antonie Book Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Modern dashboard styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main {
        padding: 2rem;
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .book-card {
        background: white;
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .action-buttons {
        display: flex;
        gap: 0.5rem;
    }
    
    .modal-overlay {
        background: rgba(0,0,0,0.5);
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "edit_book_id" not in st.session_state:
    st.session_state.edit_book_id = None
if "show_edit_modal" not in st.session_state:
    st.session_state.show_edit_modal = False
if "show_create_author_modal" not in st.session_state:
    st.session_state.show_create_author_modal = False
if "book_created" not in st.session_state:
    st.session_state.book_created = False
if "book_form_key" not in st.session_state:
    st.session_state.book_form_key = 0

# Get API client
try:
    client = get_client()
    health = client.health()
except Exception as e:
    st.error(f"❌ Failed to connect to API: {e}")
    st.stop()

# Dashboard Header
st.markdown("""
    <div class="dashboard-header">
        <h1>📚 Book Catalog Dashboard</h1>
        <p>Manage your book collection with ease</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Navigation with modern styling
with st.sidebar:
    st.markdown("# 🚀 Navigation")
    st.divider()
    
    page = st.radio(
        "Select Page",
        ["📖 Books", "✍️ Create Book", "👥 Authors", "🏢 Publishers"],
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

# Edit Book Modal
def edit_book_modal(book_id):
    try:
        book = client.get_book(book_id)
        
        # Fetch available authors
        authors_response = client.list_authors(limit=100)
        available_authors = {author["id"]: author["name"] for author in authors_response.get("items", [])}
        
        st.write("### Book Details")
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title", value=book["title"], key="edit_title")
            publisher = st.text_input("Publisher", value=book["publisher"], key="edit_publisher")
        
        with col2:
            pages = st.number_input("Pages", value=book["pages"], min_value=1, key="edit_pages")
            if available_authors:
                author_options = [f"{aid}: {name}" for aid, name in sorted(available_authors.items())]
                current_author = f"{book['author_id']}: {available_authors.get(book['author_id'], 'Unknown')}"
                selected_author = st.selectbox("Author", options=author_options, 
                                             index=author_options.index(current_author) if current_author in author_options else 0,
                                             key="edit_author")
                author_id = int(selected_author.split(":")[0])
            else:
                author_id = book['author_id']
        
        tags_input = st.text_input("Tags (comma-separated)", value=", ".join(book.get("tags", [])), key="edit_tags")
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Update Book", use_container_width=True):
                try:
                    update_data = {
                        "title": title,
                        "publisher": publisher,
                        "pages": pages,
                        "tags": tags if tags != [""] else [],
                        "author_id": author_id,
                    }
                    client.update_book(book_id, update_data)
                    st.success("✅ Book updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update: {e}")
        
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.rerun()
    
    except Exception as e:
        st.error(f"Error loading book: {e}")

# Create Author Modal
def create_author_modal():
    st.write("### Add a New Author")

    col1, col2 = st.columns(2)
    with col1:
        author_id = st.number_input("Author ID", min_value=1, step=1, value=100, key="new_author_id")
        name = st.text_input("Name", key="new_author_name", placeholder="e.g., Stephen King")

    with col2:
        birth_date = st.date_input("Birth Date (optional)", key="new_author_birth")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Add Author", use_container_width=True):
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
                    st.success("✅ Author added successfully!")
                    st.rerun()
                except Exception as e:
                    error_str = str(e)
                    if "409" in error_str or "already exists" in error_str:
                        st.error(f"❌ Author ID {author_id} already exists. Please use a different ID.")
                    elif "500" in error_str or "Internal Server Error" in error_str:
                        st.error(f"❌ Server error occurred. Please try again later.")
                    else:
                        st.error(f"❌ Failed to add author: {e}")

    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

# PAGE: Books
if page == "📖 Books":
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
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", total)
        with col2:
            st.metric("Current Page", page_num)
        with col3:
            st.metric("Results on Page", len(response["items"]))
        
        st.divider()
        
        if response["items"]:
            for book in response["items"]:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.subheader(f"📕 {book['title']}")
                        st.write(f"👤 **Author ID:** {book['author_id']}")
                        st.write(f"🏢 **Publisher:** {book['publisher']}")
                        st.write(f"📄 **Pages:** {book['pages']}")
                        if book.get("tags"):
                            st.write(f"🏷️ **Tags:** {', '.join(book['tags'])}")
                    
                    with col2:
                        st.write(f"📅 Created: {book['created_at'][:10]}")
                        st.write(f"🔄 Updated: {book['updated_at'][:10]}")
                    
                    with col3:
                        if st.button("✏️ Edit", key=f"edit_{book['id']}", use_container_width=True):
                            edit_book_modal(book['id'])
                        if st.button("🗑️ Delete", key=f"delete_{book['id']}", use_container_width=True):
                            try:
                                client.delete_book(book["id"])
                                st.success("✅ Book deleted!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to delete: {e}")
        else:
            st.info("📭 No books found")
    
    except Exception as e:
        st.error(f"Error loading books: {e}")

# PAGE: Create Book
elif page == "✍️ Create Book":
    st.header("➕ Create New Book")

    # Display success message if book was just created
    if st.session_state.book_created:
        st.success("✅ Book created successfully!")
        st.balloons()
        st.session_state.book_created = False
        st.divider()

    try:
        authors_response = client.list_authors(limit=100)
        available_authors = {author["id"]: author["name"] for author in authors_response.get("items", [])}

        if not available_authors:
            st.error("❌ No authors available. Please add authors first.")
        else:
            st.info(f"ℹ️ Available authors: {', '.join([f'{aid}: {name}' for aid, name in available_authors.items()])}")

            # Initialize session state for form persistence
            if "book_form_data" not in st.session_state:
                st.session_state.book_form_data = {"title": "", "publisher": "", "pages": None, "tags": ""}

            # Fetch the next book ID automatically
            try:
                next_id_response = client.get_next_book_id()
                next_book_id = next_id_response.get("next_id", 1)
                st.info(f"ℹ️ Next Book ID: **{next_book_id}** (auto-generated)")
            except Exception as e:
                st.error(f"❌ Failed to fetch next Book ID: {e}")
                next_book_id = 1

            with st.form("create_book_form"):
                col1, col2 = st.columns(2)

                with col1:
                    title = st.text_input("Title", value=st.session_state.book_form_data["title"], placeholder="e.g., The Great Gatsby")
                    author_options = [f"{aid}: {name}" for aid, name in sorted(available_authors.items())]
                    selected_author = st.selectbox("Select Author", options=author_options)
                    author_id = int(selected_author.split(":")[0])

                with col2:
                    publisher = st.text_input("Publisher", value=st.session_state.book_form_data["publisher"], placeholder="e.g., Penguin Books")
                    pages = st.number_input("Pages", min_value=1, step=1, value=st.session_state.book_form_data["pages"], placeholder="300")

                tags_input = st.text_input("Tags (comma-separated)", value=st.session_state.book_form_data["tags"], placeholder="e.g., Fiction, Classic, Drama")

                tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

                if st.form_submit_button("📚 Create Book", use_container_width=True):
                    if not title or not publisher or pages is None:
                        st.error("❌ All fields are required")
                    else:
                        try:
                            book_data = {
                                "id": next_book_id,
                                "title": title,
                                "author_id": author_id,
                                "publisher": publisher,
                                "pages": int(pages),
                                "tags": tags if tags != [""] else [],
                            }
                            client.create_book(book_data)
                            # Clear form data on success
                            st.session_state.book_form_data = {"title": "", "publisher": "", "pages": None, "tags": ""}
                            st.session_state.book_created = True
                            st.rerun()
                        except Exception as e:
                            # Save form data on error so user doesn't lose it
                            st.session_state.book_form_data = {"title": title, "publisher": publisher, "pages": pages, "tags": tags_input}
                            error_str = str(e)
                            if "409" in error_str or "already exists" in error_str:
                                st.error(f"⚠️ Book ID {next_book_id} is already in use. Please refresh and try again.")
                            elif "422" in error_str:
                                st.error(f"❌ Invalid data provided. Please check all fields are correct.")
                            else:
                                st.error(f"❌ Failed to create book: {e}")

    except Exception as e:
        st.error(f"Error: {e}")

# PAGE: Authors
elif page == "👥 Authors":
    st.header("👥 Author Management")

    # Add New Author Section
    with st.expander("➕ Add New Author", expanded=False):
        create_author_modal()

    st.divider()
    
    try:
        response = client.list_authors(page=1, limit=100)
        
        st.metric("Total Authors", response.get("total", 0))
        st.divider()
        
        if response["items"]:
            col1, col2, col3 = st.columns(3)
            
            for i, author in enumerate(response["items"]):
                with col1 if i % 3 == 0 else (col2 if i % 3 == 1 else col3):
                    with st.container(border=True):
                        st.subheader(f"👤 {author['name']}")
                        st.write(f"**ID:** {author['id']}")
                        if author.get("birth_date"):
                            st.write(f"**Born:** {author['birth_date']}")
                        st.write(f"**Books:** {author['book_count']}")
        else:
            st.info("📭 No authors found")
    
    except Exception as e:
        st.error(f"Error: {e}")

# PAGE: Publishers
elif page == "🏢 Publishers":
    st.header("🏢 Publisher Analytics")
    
    try:
        # Get all books to extract unique publishers
        books_response = client.list_books(limit=100)
        all_books = books_response.get("items", [])
        publishers = sorted(set(book.get("publisher", "") for book in all_books if book.get("publisher")))
        
        if publishers:
            selected_publisher = st.selectbox(
                "📍 Select Publisher",
                options=publishers,
                help="Choose a publisher to view statistics"
            )
            
            st.divider()
            
            if selected_publisher:
                try:
                    result = client.get_publisher_average_pages(selected_publisher)
                    
                    # Display publisher stats in cards
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📍 Publisher", result["publisher"])
                    
                    with col2:
                        st.metric("📄 Average Pages", f"{result['average_pages']:.0f}")
                    
                    with col3:
                        st.metric("📚 Total Books", result.get("book_count", 0))
                    
                    st.divider()
                    
                    # Show books by this publisher
                    st.subheader(f"📚 Books by {selected_publisher}")
                    publisher_books = [book for book in all_books if book.get("publisher") == selected_publisher]
                    
                    if publisher_books:
                        for book in publisher_books:
                            st.write(f"• **{book['title']}** - {book['pages']} pages")
                    else:
                        st.info("No books found")
                
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("📭 No publishers found")
    
    except Exception as e:
        st.error(f"Error loading publishers: {e}")

# Footer
st.divider()
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.9rem;">
        📚 **Book Catalog Dashboard** | Built by Shubham Godha | Powered by Streamlit & FastAPI
    </div>
    """, unsafe_allow_html=True)
