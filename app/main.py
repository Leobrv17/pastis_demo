"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.api.error_handlers import (
    general_exception_handler,
    library_exception_handler,
    validation_exception_handler,
)
from app.api.routes.books import router as books_router
from app.config import settings
from app.core.database import db
from app.core.exceptions import LibraryException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    logger.info("Starting up Library API...")
    await db.connect()
    await db.create_indexes()
    logger.info("Library API started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Library API...")
    await db.disconnect()
    logger.info("Library API shut down successfully")


# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(LibraryException, library_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(books_router, prefix="/api/v1")


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Library API",
        "version": settings.api_version
    }


# Root endpoint
@app.get("/", tags=["root"])
async def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Welcome to the Library API",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }