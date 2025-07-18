"""Book API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from app.config import settings
from app.schemas.book import (
    BookCreate,
    BookListResponse,
    BookResponse,
    BookStats,
    BookUpdate,
    BorrowRequest,
)
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


def get_book_service() -> BookService:
    """Dependency to get book service."""
    return BookService()


@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Add a new book to the library collection"
)
async def create_book(
    book_data: BookCreate,
    service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Create a new book."""
    return await service.create_book(book_data)


@router.get(
    "/",
    response_model=BookListResponse,
    summary="Get all books",
    description="Get a paginated list of books with optional filtering"
)
async def get_books(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        settings.default_page_size,
        ge=1,
        le=settings.max_page_size,
        description="Number of books per page"
    ),
    search: Optional[str] = Query(None, description="Search in title, author, or description"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    author: Optional[str] = Query(None, description="Filter by author"),
    available: Optional[bool] = Query(None, description="Filter by availability"),
    service: BookService = Depends(get_book_service)
) -> BookListResponse:
    """Get books with filtering and pagination."""
    return await service.get_books(
        page=page,
        page_size=page_size,
        search=search,
        genre=genre,
        author=author,
        available=available
    )


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get a book by ID",
    description="Get detailed information about a specific book"
)
async def get_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Get a book by ID."""
    return await service.get_book(book_id)


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update a book",
    description="Update book information"
)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Update a book."""
    return await service.update_book(book_id, book_data)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    description="Remove a book from the library collection"
)
async def delete_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
) -> None:
    """Delete a book."""
    await service.delete_book(book_id)


@router.post(
    "/{book_id}/borrow",
    response_model=BookResponse,
    summary="Borrow a book",
    description="Borrow an available book from the library"
)
async def borrow_book(
    book_id: str,
    borrow_data: BorrowRequest,
    service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Borrow a book."""
    return await service.borrow_book(book_id, borrow_data)


@router.post(
    "/{book_id}/return",
    response_model=BookResponse,
    summary="Return a book",
    description="Return a borrowed book to the library"
)
async def return_book(
    book_id: str,
    service: BookService = Depends(get_book_service)
) -> BookResponse:
    """Return a borrowed book."""
    return await service.return_book(book_id)


@router.get(
    "/search/query",
    response_model=List[BookResponse],
    summary="Search books",
    description="Search books by text query in title, author, or description"
)
async def search_books(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    service: BookService = Depends(get_book_service)
) -> List[BookResponse]:
    """Search books by text query."""
    return await service.search_books(q, limit)


@router.get(
    "/statistics/overview",
    response_model=BookStats,
    summary="Get library statistics",
    description="Get comprehensive statistics about the library collection"
)
async def get_statistics(
    service: BookService = Depends(get_book_service)
) -> BookStats:
    """Get library statistics."""
    return await service.get_statistics()