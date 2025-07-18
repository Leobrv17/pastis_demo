"""Book repository for database operations."""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from beanie import PydanticObjectId
from beanie.operators import In, Text
from pymongo import DESCENDING

from app.core.exceptions import BookNotFoundError
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class BookRepository:
    """Repository for book database operations."""

    @staticmethod
    async def create(book_data: BookCreate) -> Book:
        """Create a new book."""
        book = Book(**book_data.model_dump())
        return await book.insert()

    @staticmethod
    async def get_by_id(book_id: str) -> Optional[Book]:
        """Get a book by ID."""
        if not PydanticObjectId.is_valid(book_id):
            return None
        return await Book.get(book_id)

    @staticmethod
    async def get_by_isbn(isbn: str) -> Optional[Book]:
        """Get a book by ISBN."""
        return await Book.find_one(Book.isbn == isbn)

    @staticmethod
    async def get_all(
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None,
        genre: Optional[str] = None,
        author: Optional[str] = None,
        available: Optional[bool] = None
    ) -> Tuple[List[Book], int]:
        """Get all books with optional filtering and pagination."""
        query = Book.find()

        # Apply filters
        if search:
            query = query.find(Text(search))

        if genre:
            query = query.find(Book.genre == genre)

        if author:
            query = query.find(Book.author.contains(author, case_insensitive=True))

        if available is not None:
            query = query.find(Book.available == available)

        # Get total count
        total = await query.count()

        # Apply pagination
        skip = (page - 1) * page_size
        books = await query.skip(skip).limit(page_size).to_list()

        return books, total

    @staticmethod
    async def update(book_id: str, book_data: BookUpdate) -> Optional[Book]:
        """Update a book."""
        book = await BookRepository.get_by_id(book_id)
        if not book:
            return None

        update_data = book_data.model_dump(exclude_unset=True)
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            await book.update({"$set": update_data})

        return await BookRepository.get_by_id(book_id)

    @staticmethod
    async def delete(book_id: str) -> bool:
        """Delete a book."""
        book = await BookRepository.get_by_id(book_id)
        if not book:
            return False

        await book.delete()
        return True

    @staticmethod
    async def get_popular_genres(limit: int = 5) -> List[Dict[str, int]]:
        """Get popular genres with book counts."""
        pipeline = [
            {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit},
            {"$project": {"genre": "$_id", "count": 1, "_id": 0}}
        ]

        result = await Book.aggregate(pipeline).to_list()
        return result

    @staticmethod
    async def get_recent_additions(limit: int = 5) -> List[Book]:
        """Get recently added books."""
        return await Book.find().sort([("created_at", DESCENDING)]).limit(limit).to_list()

    @staticmethod
    async def get_overdue_books() -> List[Book]:
        """Get overdue books."""
        now = datetime.utcnow()
        return await Book.find(
            Book.available == False,
            Book.due_date < now
        ).to_list()

    @staticmethod
    async def search_books(query: str, limit: int = 10) -> List[Book]:
        """Search books by title, author, or description."""
        return await Book.find(Text(query)).limit(limit).to_list()