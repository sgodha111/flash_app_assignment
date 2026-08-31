"""Book schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """Base book schema."""

    title: str = Field(..., min_length=1, max_length=500)
    author_id: int = Field(..., gt=0)
    publisher: str = Field(..., min_length=1, max_length=255)
    pages: int = Field(..., gt=0, le=100000)
    tags: List[str] = Field(default_factory=list, max_length=20)


class BookCreate(BookBase):
    """Schema for creating a book."""

    id: int = Field(..., gt=0)


class BookUpdate(BaseModel):
    """Schema for updating a book (partial update)."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    publisher: Optional[str] = Field(None, min_length=1, max_length=255)
    pages: Optional[int] = Field(None, gt=0, le=100000)
    tags: Optional[List[str]] = Field(None, max_length=20)
    author_id: Optional[int] = Field(None, gt=0)


class BookResponse(BookBase):
    """Schema for book response."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class BookListResponse(BaseModel):
    """Paginated list of books."""

    items: List[BookResponse]
    page: int
    limit: int
    total: int
