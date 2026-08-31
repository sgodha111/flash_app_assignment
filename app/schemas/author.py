"""Author schemas."""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    """Base author schema."""

    name: str = Field(..., min_length=1, max_length=255)
    birth_date: Optional[date] = None


class AuthorCreate(AuthorBase):
    """Schema for creating an author."""

    id: int = Field(..., gt=0)


class AuthorResponse(AuthorBase):
    """Schema for author response."""

    id: int

    class Config:
        """Pydantic config."""

        from_attributes = True


class AuthorWithBookCount(AuthorResponse):
    """Author with book count."""

    book_count: int = 0


class AuthorListResponse(BaseModel):
    """Paginated list of authors."""

    items: List[AuthorWithBookCount]
    page: int
    limit: int
    total: int
