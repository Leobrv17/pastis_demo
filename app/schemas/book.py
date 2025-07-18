"""Book schemas for request/response validation."""

from datetime import datetime
from typing import List, Optional
import re

from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    """Base book schema."""

    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(..., min_length=10, max_length=17)
    publication_year: int = Field(..., ge=1000, le=2024)
    genre: str = Field(..., min_length=1, max_length=50)
    pages: int = Field(..., gt=0, le=10000)
    description: Optional[str] = Field(None, max_length=1000)


class BookCreate(BookBase):
    """Schema for creating a book."""

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        """Validate ISBN format."""
        # Remove hyphens and spaces
        digits_only = re.sub(r'[-\s]', '', v)
        if not digits_only.isdigit():
            raise ValueError('ISBN must contain only digits and hyphens')
        if len(digits_only) not in [10, 13]:
            raise ValueError('ISBN must be 10 or 13 digits')
        return v


class BookUpdate(BaseModel):
    """Schema for updating a book."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=17)
    publication_year: Optional[int] = Field(None, ge=1000, le=2024)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    pages: Optional[int] = Field(None, gt=0, le=10000)
    description: Optional[str] = Field(None, max_length=1000)
    available: Optional[bool] = None

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: Optional[str]) -> Optional[str]:
        """Validate ISBN format."""
        if v is None:
            return v
        # Remove hyphens and spaces
        digits_only = re.sub(r'[-\s]', '', v)
        if not digits_only.isdigit():
            raise ValueError('ISBN must contain only digits and hyphens')
        if len(digits_only) not in [10, 13]:
            raise ValueError('ISBN must be 10 or 13 digits')
        return v


class BookResponse(BookBase):
    """Schema for book response."""

    id: str = Field(..., alias="_id")
    available: bool
    borrowed_by: Optional[str]
    borrowed_date: Optional[datetime]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class BookListResponse(BaseModel):
    """Schema for paginated book list response."""

    books: List[BookResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class BorrowRequest(BaseModel):
    """Schema for borrowing a book."""

    borrower_name: str = Field(..., min_length=1, max_length=100)
    days: int = Field(14, ge=1, le=90, description="Nombre de jours d'emprunt")


class BookStats(BaseModel):
    """Schema for book statistics."""

    total_books: int
    available_books: int
    borrowed_books: int
    overdue_books: int
    popular_genres: List[dict]
    recent_additions: List[BookResponse]