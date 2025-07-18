"""Book model definition."""

from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import Field


class Book(Document):
    """Book document model."""

    title: str = Field(..., description="Titre du livre")
    author: str = Field(..., description="Auteur du livre")
    isbn: str = Field(..., description="ISBN du livre")
    publication_year: int = Field(..., description="Année de publication")
    genre: str = Field(..., description="Genre du livre")
    pages: int = Field(..., gt=0, description="Nombre de pages")
    description: Optional[str] = Field(None, description="Description du livre")
    available: bool = Field(True, description="Disponibilité du livre")
    borrowed_by: Optional[str] = Field(None, description="Emprunté par")
    borrowed_date: Optional[datetime] = Field(None, description="Date d'emprunt")
    due_date: Optional[datetime] = Field(None, description="Date de retour prévue")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "books"
        # Indexes basiques - beanie 1.20.0 les créera automatiquement
        indexes = [
            "isbn",
            "title",
            "author",
            "genre",
            "available"
        ]

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    def is_overdue(self) -> bool:
        """Check if the book is overdue."""
        if not self.borrowed_date or not self.due_date:
            return False
        return datetime.utcnow() > self.due_date