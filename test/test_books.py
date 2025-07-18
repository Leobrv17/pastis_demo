"""Tests for book operations."""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.book import BookCreate


@pytest.fixture
def test_client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def sample_book_data():
    """Sample book data for testing."""
    return {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "1234567890",
        "publication_year": 2023,
        "genre": "Fiction",
        "pages": 200,
        "description": "A test book for unit testing"
    }


class TestBookOperations:
    """Test class for book operations."""

    def test_health_check(self, test_client):
        """Test health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self, test_client):
        """Test root endpoint."""
        response = test_client.get("/")
        assert response.status_code == 200
        assert "Welcome to the Library API" in response.json()["message"]

    @pytest.mark.asyncio
    async def test_create_book(self, sample_book_data):
        """Test book creation."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/v1/books/", json=sample_book_data)
            assert response.status_code == 201
            data = response.json()
            assert data["title"] == sample_book_data["title"]
            assert data["author"] == sample_book_data["author"]
            assert data["available"] is True

    @pytest.mark.asyncio
    async def test_get_books(self):
        """Test getting books list."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/books/")
            assert response.status_code == 200
            data = response.json()
            assert "books" in data
            assert "total" in data
            assert "page" in data

    def test_book_validation(self, test_client):
        """Test book data validation."""
        invalid_data = {
            "title": "",  # Empty title should fail
            "author": "Test Author",
            "isbn": "123",  # Too short ISBN
            "publication_year": 3000,  # Future year
            "genre": "Fiction",
            "pages": -10,  # Negative pages
        }

        response = test_client.post("/api/v1/books/", json=invalid_data)
        assert response.status_code == 422


@pytest.mark.asyncio
class TestAsyncBookOperations:
    """Async test class for complex book operations."""

    async def test_borrow_and_return_flow(self, sample_book_data):
        """Test complete borrow and return workflow."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Create a book
            create_response = await client.post("/api/v1/books/", json=sample_book_data)
            assert create_response.status_code == 201
            book_id = create_response.json()["id"]

            # Borrow the book
            borrow_data = {"borrower_name": "John Doe", "days": 14}
            borrow_response = await client.post(
                f"/api/v1/books/{book_id}/borrow",
                json=borrow_data
            )
            assert borrow_response.status_code == 200
            borrow_result = borrow_response.json()
            assert borrow_result["available"] is False
            assert borrow_result["borrowed_by"] == "John Doe"

            # Return the book
            return_response = await client.post(f"/api/v1/books/{book_id}/return")
            assert return_response.status_code == 200
            return_result = return_response.json()
            assert return_result["available"] is True
            assert return_result["borrowed_by"] is None

    async def test_search_functionality(self, sample_book_data):
        """Test book search functionality."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Create a book
            await client.post("/api/v1/books/", json=sample_book_data)

            # Search for the book
            response = await client.get("/api/v1/books/search/query?q=Test Book")
            assert response.status_code == 200
            results = response.json()
            assert len(results) > 0
            assert any(book["title"] == "Test Book" for book in results)

    async def test_statistics_endpoint(self):
        """Test statistics endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/books/statistics/overview")
            assert response.status_code == 200
            stats = response.json()
            assert "total_books" in stats
            assert "available_books" in stats
            assert "borrowed_books" in stats
            assert "popular_genres" in stats