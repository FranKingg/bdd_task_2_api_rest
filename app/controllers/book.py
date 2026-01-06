"""Controller for Book endpoints."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Sequence

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from advanced_alchemy.filters import LimitOffset
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException
from litestar.params import Parameter

from app.controllers import duplicate_error_handler, not_found_error_handler
from app.dtos.book import BookCreateDTO, BookReadDTO, BookUpdateDTO
from app.models import Book, BookStats
from app.repositories.book import BookRepository, provide_book_repo

ALLOWED_LANGUAGES = {"es", "en", "fr"}


class BookController(Controller):
    """Controller for book management operations."""

    path = "/books"
    tags = ["books"]
    return_dto = BookReadDTO
    dependencies = {"books_repo": Provide(provide_book_repo)}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_books(self, books_repo: BookRepository) -> Sequence[Book]:
        """Get all books."""
        return books_repo.list()

    @get("/{id:int}")
    async def get_book(self, id: int, books_repo: BookRepository) -> Book:
        """Get a book by ID."""
        return books_repo.get(id)

    @post("/", dto=BookCreateDTO)
    async def create_book(
        self,
        data: DTOData[Book],
        books_repo: BookRepository,
    ) -> Book:
        """Create a new book."""
        payload = data.as_builtins()

        published_year = int(payload.get("published_year"))
        current_year = date.today().year
        if not (1000 <= published_year <= current_year):
            raise HTTPException(
                detail=f"El año de publicación debe estar entre 1000 y {current_year}",
                status_code=400,
            )

        stock = int(payload.get("stock", 1))
        if stock <= 0:
            raise HTTPException(detail="stock debe ser mayor a 0", status_code=400)

        language = payload.get("language")
        if language is not None and str(language) not in ALLOWED_LANGUAGES:
            raise HTTPException(detail="language debe ser uno de: es, en, fr", status_code=400)

        return books_repo.add(Book(**payload))

    @patch("/{id:int}", dto=BookUpdateDTO)
    async def update_book(
        self,
        id: int,
        data: DTOData[Book],
        books_repo: BookRepository,
    ) -> Book:
        """Update a book by ID."""
        payload = data.as_builtins()

        if "stock" in payload and payload["stock"] is not None:
            if int(payload["stock"]) < 0:
                raise HTTPException(detail="stock no puede ser negativo", status_code=400)

        if "language" in payload and payload["language"] is not None:
            if str(payload["language"]) not in ALLOWED_LANGUAGES:
                raise HTTPException(detail="language debe ser uno de: es, en, fr", status_code=400)

        book, _ = books_repo.get_and_update(match_fields="id", id=id, **payload)
        return book

    @delete("/{id:int}")
    async def delete_book(self, id: int, books_repo: BookRepository) -> None:
        """Delete a book by ID."""
        books_repo.delete(id)

    # ---- Métodos requeridos por la tarea (repositorio + endpoints) ----

    @get("/available")
    async def get_available_books(self, books_repo: BookRepository) -> Sequence[Book]:
        """Return books with stock > 0."""
        return books_repo.get_available_books()

    @get("/by-category/{category_id:int}")
    async def get_books_by_category(self, category_id: int, books_repo: BookRepository) -> Sequence[Book]:
        return books_repo.find_by_category(category_id)

    @get("/most-reviewed")
    async def get_most_reviewed_books(
        self,
        limit: Annotated[int, Parameter(query="limit", default=10, ge=1, le=100)],
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        return books_repo.get_most_reviewed_books(limit=limit)

    @patch("/{id:int}/stock")
    async def update_book_stock(
        self,
        id: int,
        quantity: Annotated[int, Parameter(query="quantity")],
        books_repo: BookRepository,
    ) -> Book:
        try:
            return books_repo.update_stock(book_id=id, quantity=quantity)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

    @get("/negative-reviews")
    async def get_books_with_negative_reviews(
        self,
        min_count: Annotated[int, Parameter(query="min_count", default=1, ge=1)],
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        return books_repo.get_books_with_negative_reviews(min_count=min_count)

    @get("/by-author")
    async def search_by_author(
        self,
        author_name: Annotated[str, Parameter(query="author_name")],
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        return books_repo.search_by_author(author_name=author_name)

    # ---- Extras que venían en el starter (se mantienen) ----

    @get("/search/")
    async def search_book_by_title(self, title: str, books_repo: BookRepository) -> Sequence[Book]:
        """Search books by title."""
        return books_repo.list(Book.title.ilike(f"%{title}%"))

    @get("/filter")
    async def filter_books_by_year(
        self,
        year_from: Annotated[int, Parameter(query="from")],
        to: int,
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Filter books by published year."""
        return books_repo.list(Book.published_year.between(year_from, to))

    @get("/recent")
    async def get_recent_books(
        self,
        limit: Annotated[int, Parameter(query="limit", default=10, ge=1, le=50)],
        books_repo: BookRepository,
    ) -> Sequence[Book]:
        """Get most recent books."""
        return books_repo.list(LimitOffset(offset=0, limit=limit), order_by=Book.created_at.desc())

    @get("/stats")
    async def get_book_stats(self, books_repo: BookRepository) -> BookStats:
        """Get statistics about books."""
        total_books = books_repo.count()
        if total_books == 0:
            return BookStats(0, 0, None, None)

        books = books_repo.list()
        average_pages = sum(book.pages for book in books) / total_books
        oldest_year = min(book.published_year for book in books)
        newest_year = max(book.published_year for book in books)

        return BookStats(
            total_books=total_books,
            average_pages=average_pages,
            oldest_publication_year=oldest_year,
            newest_publication_year=newest_year,
        )
