"""Book service layer for business logic."""

import math
from datetime import datetime, timedelta
from typing import List, Tuple

from app.core.exceptions import (
    BookAlreadyExistsError,
    BookNotAvailableError,
    BookNotBorrowedError,
    BookNotFoundError,
)
from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import (
    BookCreate,
    BookListResponse,
    BookResponse,
    BookStats,
    BookUpdate,
    BorrowRequest,
)


class BookService:
    """Service for book business logic."""

    def __init__(self):
        self.repository = BookRepository()

    async def create_book(self, book_data: BookCreate) -> BookResponse:
        """Create a new book."""
        # Check if book already exists
        existing_book = await self.repository.get_by_isbn(book_data.isbn)
        if existing_book:
            raise BookAlreadyExistsError(book_data.isbn)

        book = await self.repository.create(book_data)
        return self._to_response(book)

    async def get_book(self, book_id: str) -> BookResponse:
        """Get a book by ID."""
        book = await self.repository.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)

        return self._to_response(book)

    async def get_books(
            self,
            page: int = 1,
            page_size: int = 10,
            search: str = None,
            genre: str = None,
            author: str = None,
            available: bool = None
    ) -> BookListResponse:
        """Get books with filtering and pagination."""
        books, total = await self.repository.get_all(
            page=page,
            page_size=page_size,
            search=search,
            genre=genre,
            author=author,
            available=available
        )

        total_pages = math.ceil(total / page_size)

        return BookListResponse(
            books=[self._to_response(book) for book in books],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def update_book(self, book_id: str, book_data: BookUpdate) -> BookResponse:
        """Update a book."""
        # Check if book exists
        if not await self.repository.get_by_id(book_id):
            raise BookNotFoundError(book_id)

        # Check ISBN uniqueness if updating ISBN
        if book_data.isbn:
            existing_book = await self.repository.get_by_isbn(book_data.isbn)
            if existing_book and str(existing_book.id) != book_id:
                raise BookAlreadyExistsError(book_data.isbn)

        book = await self.repository.update(book_id, book_data)
        return self._to_response(book)

    async def delete_book(self, book_id: str) -> bool:
        """Delete a book."""
        if not await self.repository.get_by_id(book_id):
            raise BookNotFoundError(book_id)

        return await self.repository.delete(book_id)

    async def borrow_book(self, book_id: str, borrow_data: BorrowRequest) -> BookResponse:
        """Borrow a book."""
        book = await self.repository.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)

        if not book.available:
            raise BookNotAvailableError(book_id)

        # Update book with borrowing information
        now = datetime.utcnow()
        due_date = now + timedelta(days=borrow_data.days)

        update_data = BookUpdate(
            available=False,
            borrowed_by=borrow_data.borrower_name,
            borrowed_date=now,
            due_date=due_date
        )

        book = await self.repository.update(book_id, update_data)
        return self._to_response(book)

    async def return_book(self, book_id: str) -> BookResponse:
        """Return a borrowed book."""
        book = await self.repository.get_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)

        if book.available:
            raise BookNotBorrowedError(book_id)

        # Update book to available
        update_data = BookUpdate(
            available=True,
            borrowed_by=None,
            borrowed_date=None,
            due_date=None
        )

        book = await self.repository.update(book_id, update_data)
        return self._to_response(book)

    async def get_statistics(self) -> BookStats:
        """Get library statistics."""
        # Get counts
        all_books, total_books = await self.repository.get_all(page_size=1)
        available_books, available_count = await self.repository.get_all(
            available=True, page_size=1
        )
        borrowed_books, borrowed_count = await self.repository.get_all(
            available=False, page_size=1
        )

        # Get overdue books
        overdue_books = await self.repository.get_overdue_books()

        # Get popular genres
        popular_genres = await self.repository.get_popular_genres()

        # Get recent additions
        recent_additions = await self.repository.get_recent_additions()

        return BookStats(
            total_books=total_books,
            available_books=available_count,
            borrowed_books=borrowed_count,
            overdue_books=len(overdue_books),
            popular_genres=popular_genres,
            recent_additions=[self._to_response(book) for book in recent_additions]
        )

    async def search_books(self, query: str, limit: int = 10) -> List[BookResponse]:
        """Search books by text query."""
        books = await self.repository.search_books(query, limit)
        return [self._to_response(book) for book in books]

    def _to_response(self, book: Book) -> BookResponse:
        """Convert Book model to BookResponse."""
        return BookResponse(
            _id=str(book.id),
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            publication_year=book.publication_year,
            genre=book.genre,
            pages=book.pages,
            description=book.description,
            available=book.available,
            borrowed_by=book.borrowed_by,
            borrowed_date=book.borrowed_date,
            due_date=book.due_date,
            created_at=book.created_at,
            updated_at=book.updated_at
        )