"""Streamlit frontend for Antonie Book Catalog API."""

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

# Configure Streamlit page
st.set_page_config(
    page_title="Antonie Book Catalog",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styling
st.markdown(
    """
    <style>
    .main { padding: 2rem; }
    .stTabs [data-baseweb="tab-list"] button { width: 100%; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("📚 Antonie Book Catalog")
st.subheader("Manage Books and Authors")

# Check API connectivity
try:
    client = get_client()
    health = client.health()
    st.success("✅ Connected to API")
except Exception as e:
    st.error(f"❌ Failed to connect to API: {e}")
    st.stop()


# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Books",
        "Create Book",
        "Authors",
        "Publishers",
    ],
)

if page == "Books":
    st.header("📖 Books")

    col1, col2, col3 = st.columns(3)

    with col1:
        search_title = st.text_input("Search by title", key="search_title")
    with col2:
        search_author = st.number_input(
            "Filter by author ID", value=0, min_value=0, step=1
        )
    with col3:
        page_num = st.number_input("Page", value=1, min_value=1, step=1)

    try:
        response = client.list_books(
            page=page_num,
            limit=10,
            title=search_title if search_title else None,
            author_id=search_author if search_author > 0 else None,
        )

        total = response.get("total", 0)
        st.info(f"Total books: {total}")

        if response["items"]:
            for book in response["items"]:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.subheader(book["title"])
                        st.write(f"**Author ID:** {book['author_id']}")
                        st.write(f"**Publisher:** {book['publisher']}")
                        st.write(f"**Pages:** {book['pages']}")
                        if book.get("tags"):
                            st.write(f"**Tags:** {', '.join(book['tags'])}")

                    with col2:
                        st.write(f"📅 Created: {book['created_at'][:10]}")
                        st.write(f"🔄 Updated: {book['updated_at'][:10]}")

                    with col3:
                        if st.button("Edit", key=f"edit_{book['id']}"):
                            st.session_state.edit_book_id = book["id"]
                            st.rerun()
                        if st.button("Delete", key=f"delete_{book['id']}"):
                            try:
                                client.delete_book(book["id"])
                                st.success("Book deleted successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to delete book: {e}")
        else:
            st.info("No books found")

        # Show edit form if a book is being edited
        if "edit_book_id" in st.session_state and st.session_state.edit_book_id:
            st.divider()
            st.subheader("✏️ Edit Book")

            try:
                book = client.get_book(st.session_state.edit_book_id)

                # Fetch available authors for edit form
                authors_response = client.list_authors(limit=100)
                available_authors = {author["id"]: author["name"] for author in authors_response.get("items", [])}

                with st.form("edit_book_form"):
                    title = st.text_input("Title", value=book["title"])
                    publisher = st.text_input("Publisher", value=book["publisher"])
                    pages = st.number_input("Pages", value=book["pages"], min_value=1)

                    # Create selectbox for author
                    if available_authors:
                        author_options = [f"{author_id}: {author_name}"
                                        for author_id, author_name in sorted(available_authors.items())]
                        current_author_str = f"{book['author_id']}: {available_authors.get(book['author_id'], 'Unknown')}"
                        selected_author = st.selectbox("Select Author", options=author_options,
                                                       index=author_options.index(current_author_str) if current_author_str in author_options else 0)
                        author_id = int(selected_author.split(":")[0])
                    else:
                        author_id = st.number_input("Author ID", value=book["author_id"], min_value=1)

                    tags_input = st.text_input("Tags (comma-separated)", value=", ".join(book.get("tags", [])))
                    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Update Book"):
                            try:
                                update_data = {
                                    "title": title,
                                    "publisher": publisher,
                                    "pages": pages,
                                    "tags": tags if tags != [""] else [],
                                    "author_id": author_id,
                                }
                                client.update_book(st.session_state.edit_book_id, update_data)
                                st.success("✅ Book updated successfully!")
                                st.session_state.edit_book_id = None
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to update book: {e}")

                    with col2:
                        if st.form_submit_button("Cancel"):
                            st.session_state.edit_book_id = None
                            st.rerun()

            except Exception as e:
                st.error(f"Error loading book: {e}")
                if st.button("Close"):
                    st.session_state.edit_book_id = None
                    st.rerun()

    except Exception as e:
        st.error(f"Error loading books: {e}")


elif page == "Create Book":
    st.header("➕ Create New Book")

    # Initialize session state for form
    if "book_created" not in st.session_state:
        st.session_state.book_created = False
    if "duplicate_id_error" not in st.session_state:
        st.session_state.duplicate_id_error = False
    if "duplicate_book_id" not in st.session_state:
        st.session_state.duplicate_book_id = None
    if "create_book_id" not in st.session_state:
        st.session_state.create_book_id = None
    if "create_title" not in st.session_state:
        st.session_state.create_title = ""
    if "create_publisher" not in st.session_state:
        st.session_state.create_publisher = ""
    if "create_pages" not in st.session_state:
        st.session_state.create_pages = 300
    if "create_tags" not in st.session_state:
        st.session_state.create_tags = ""
    if "create_author_idx" not in st.session_state:
        st.session_state.create_author_idx = 0
    if "form_key" not in st.session_state:
        st.session_state.form_key = 0

    # Show success message if book was just created
    if st.session_state.book_created:
        st.success("✅ Book created successfully! Form cleared for next entry.", icon="✅")
        st.session_state.book_created = False
        st.session_state.duplicate_id_error = False
        st.session_state.duplicate_book_id = None
    else:
        # Clear error flag when NOT showing success (fresh page load with no error)
        if st.session_state.duplicate_id_error:
            # Only keep error if we explicitly set it
            pass
        else:
            # No error, ensure everything is clean
            st.session_state.duplicate_id_error = False
            st.session_state.duplicate_book_id = None

    # Show duplicate ID error
    if st.session_state.duplicate_id_error:
        st.markdown("""
        <div style='background-color: #ff4444; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
            <b>🚫 Book ID Already Exists!</b><br>
            Book ID <b>{}</b> is already in use. Please use a different ID.
        </div>
        """.format(st.session_state.duplicate_book_id), unsafe_allow_html=True)

    # Fetch available authors
    try:
        authors_response = client.list_authors(limit=100)
        available_authors = {author["id"]: author["name"] for author in authors_response.get("items", [])}

        if not available_authors:
            st.error("❌ No authors available. Please add authors first.")
        else:
            st.info(f"ℹ️ Available authors: {', '.join([f'{aid}: {name}' for aid, name in available_authors.items()])}")

            with st.form(f"create_book_form_{st.session_state.form_key}"):
                # Highlight Book ID field if there's a duplicate error
                book_id_default = st.session_state.create_book_id if st.session_state.create_book_id and st.session_state.create_book_id > 0 else 1

                if st.session_state.duplicate_id_error:
                    st.markdown("<p style='color: red;'><b>Book ID (Already Exists!)</b></p>", unsafe_allow_html=True)
                    book_id = st.number_input(
                        "label_book_id",
                        min_value=1,
                        step=1,
                        value=book_id_default,
                        label_visibility="collapsed",
                    )
                else:
                    book_id = st.number_input(
                        "Book ID",
                        min_value=1,
                        step=1,
                        value=book_id_default
                    )

                title = st.text_input(
                    "Title",
                    max_chars=500,
                    value=st.session_state.create_title,
                    placeholder="e.g., Advanced Python"
                )

                # Create selectbox for author instead of number input
                author_options = [f"{author_id}: {author_name}"
                                for author_id, author_name in sorted(available_authors.items())]
                selected_author = st.selectbox(
                    "Select Author",
                    options=author_options,
                    index=st.session_state.create_author_idx
                )
                author_id = int(selected_author.split(":")[0])

                publisher = st.text_input(
                    "Publisher",
                    max_chars=255,
                    value=st.session_state.create_publisher,
                    placeholder="e.g., O'Reilly Media"
                )
                pages = st.number_input(
                    "Pages",
                    min_value=1,
                    step=1,
                    value=st.session_state.create_pages
                )
                tags_input = st.text_input(
                    "Tags (comma-separated)",
                    value=st.session_state.create_tags,
                    placeholder="e.g., Python, Advanced, Development"
                )

                tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

                if st.form_submit_button("Create Book"):
                    # CRITICAL: If trying a DIFFERENT Book ID than what caused the error, CLEAR the error immediately
                    if st.session_state.duplicate_id_error:
                        if st.session_state.duplicate_book_id is not None and book_id != st.session_state.duplicate_book_id:
                            # Different ID - clear the old error!
                            st.session_state.duplicate_id_error = False
                            st.session_state.duplicate_book_id = None

                    if not title or not publisher:
                        st.error("❌ Title and Publisher are required")
                    else:
                        try:
                            book_data = {
                                "id": book_id,
                                "title": title,
                                "author_id": author_id,
                                "publisher": publisher,
                                "pages": pages,
                                "tags": tags if tags != [""] else [],
                            }

                            client.create_book(book_data)

                            # Clear form fields in session state
                            st.session_state.create_book_id = None  # Blank field
                            st.session_state.create_title = ""
                            st.session_state.create_publisher = ""
                            st.session_state.create_pages = 300
                            st.session_state.create_tags = ""
                            st.session_state.create_author_idx = 0
                            st.session_state.book_created = True
                            st.session_state.duplicate_id_error = False
                            st.session_state.duplicate_book_id = None
                            st.session_state.form_key += 1  # Change form key to force form recreation

                            st.rerun()

                        except Exception as e:
                            error_str = str(e)
                            # Check if it's a 409 Conflict (duplicate ID)
                            if "409" in error_str or "already exists" in error_str.lower():
                                st.session_state.duplicate_id_error = True
                                st.session_state.duplicate_book_id = book_id
                                st.error(f"🔴 Book ID {book_id} already exists! Please use a different ID.")
                            else:
                                st.error(f"Failed to create book: {e}")
    except Exception as e:
        st.error(f"❌ Error loading authors: {e}")


elif page == "Authors":
    st.header("👥 Authors")

    try:
        response = client.list_authors(page=1, limit=100)

        if response["items"]:
            for author in response["items"]:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.subheader(author["name"])
                        st.write(f"**Author ID:** {author['id']}")
                        if author.get("birth_date"):
                            st.write(f"**Born:** {author['birth_date']}")
                        st.write(f"**Books written:** {author['book_count']}")

                    with col2:
                        if st.button("View Books", key=f"author_books_{author['id']}"):
                            st.session_state.view_author_id = author["id"]

            if "view_author_id" in st.session_state:
                st.divider()
                st.subheader(f"Books by Author {st.session_state.view_author_id}")
                try:
                    books = client.get_author_books(st.session_state.view_author_id)
                    if books:
                        for book in books:
                            st.write(f"- {book['title']} ({book['pages']} pages)")
                    else:
                        st.info("No books by this author")
                except Exception as e:
                    st.error(f"Error loading books: {e}")
        else:
            st.info("No authors found")

    except Exception as e:
        st.error(f"Error loading authors: {e}")


elif page == "Publishers":
    st.header("🏢 Publishers")

    publisher_name = st.text_input("Enter publisher name")

    if publisher_name:
        try:
            result = client.get_publisher_average_pages(publisher_name)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Publisher", result["publisher"])
            with col2:
                st.metric("Average Pages", f"{result['average_pages']:.0f}")
            with col3:
                st.metric("Total Books", result.get("book_count", 0))

        except Exception as e:
            st.error(f"Publisher not found or error: {e}")
    else:
        st.info("Enter a publisher name to see statistics")


st.divider()
st.caption("Antonie Book Catalog - Built with Streamlit & FastAPI")
