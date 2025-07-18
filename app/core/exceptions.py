"""Custom exceptions for the library API."""

from typing import Any, Dict, Optional


class LibraryException(Exception):
    """Base exception for library operations."""

    def __init__(self, message: str, status_code: int = 500, detail: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(self.message)


class BookNotFoundError(LibraryException):
    """Exception raised when a book is not found."""

    def __init__(self, book_id: str):
        super().__init__(
            message=f"Book with ID '{book_id}' not found",
            status_code=404
        )


class BookAlreadyExistsError(LibraryException):
    """Exception raised when trying to create a book that already exists."""

    def __init__(self, isbn: str):
        super().__init__(
            message=f"Book with ISBN '{isbn}' already exists",
            status_code=409
        )


class BookNotAvailableError(LibraryException):
    """Exception raised when trying to borrow an unavailable book."""

    def __init__(self, book_id: str):
        super().__init__(
            message=f"Book with ID '{book_id}' is not available for borrowing",
            status_code=400
        )


class BookNotBorrowedError(LibraryException):
    """Exception raised when trying to return a book that is not borrowed."""

    def __init__(self, book_id: str):
        super().__init__(
            message=f"Book with ID '{book_id}' is not currently borrowed",
            status_code=400
        )


class ValidationError(LibraryException):
    """Exception raised for validation errors."""

    def __init__(self, message: str, errors: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=422,
            detail=errors or {}
        )