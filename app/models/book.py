"""Définition du modèle Book."""

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class Book(Document):
    """Modèle de document Book."""

    title: Indexed(str) = Field(..., description="Titre du livre")
    author: Indexed(str) = Field(..., description="Auteur du livre")
    isbn: Indexed(str) = Field(..., description="ISBN du livre")
    publication_year: int = Field(..., description="Année de publication")
    genre: Indexed(str) = Field(..., description="Genre du livre")
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
        use_state_management = True
        indexes = [
            "isbn",
            "title",
            "author",
            "genre",
            "available",
            [("title", "text"), ("author", "text"), ("description", "text")]  # Index de recherche textuelle
        ]

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    def is_overdue(self) -> bool:
        """Vérifier si le livre est en retard."""
        if not self.borrowed_date or not self.due_date:
            return False
        return datetime.utcnow() > self.due_date