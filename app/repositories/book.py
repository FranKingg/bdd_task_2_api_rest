"""Repository for Book database operations."""

from __future__ import annotations

from typing import Sequence

from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Book, Category, Review, book_categories


class BookRepository(SQLAlchemySyncRepository[Book]):
    """Repository for book database operations."""

    model_type = Book

    def get_available_books(self) -> Sequence[Book]:
        """Return books with stock > 0."""
        stmt = select(Book).where(Book.stock > 0).order_by(Book.title.asc())
        return list(self.session.scalars(stmt).all())

    def find_by_category(self, category_id: int) -> Sequence[Book]:
        """Return books belonging to a category."""
        stmt = (
            select(Book)
            .join(book_categories, book_categories.c.book_id == Book.id)
            .where(book_categories.c.category_id == category_id)
            .order_by(Book.title.asc())
        )
        return list(self.session.scalars(stmt).all())

    def get_most_reviewed_books(self, limit: int = 10) -> Sequence[Book]:
        """Return books ordered by number of reviews."""
        stmt = (
            select(Book)
            .outerjoin(Review, Review.book_id == Book.id)
            .group_by(Book.id)
            .order_by(func.count(Review.id).desc(), Book.title.asc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt).all())

    def update_stock(self, book_id: int, quantity: int) -> Book:
        """Add quantity to stock (can be negative). Stock can't go below 0."""
        book = self.get(book_id)
        new_stock = (book.stock or 0) + quantity
        if new_stock < 0:
            raise ValueError("Stock no puede ser negativo")
        book.stock = new_stock
        self.update(book)
        return book

    def get_books_with_negative_reviews(self, min_count: int = 1) -> Sequence[Book]:
        """Return books that have at least `min_count` negative reviews (rating <= 2)."""
        stmt = (
            select(Book)
            .join(Review, Review.book_id == Book.id)
            .where(Review.rating <= 2)
            .group_by(Book.id)
            .having(func.count(Review.id) >= min_count)
            .order_by(func.count(Review.id).desc(), Book.title.asc())
        )
        return list(self.session.scalars(stmt).all())

    def search_by_author(self, author_name: str) -> Sequence[Book]:
        """Search books by author name (partial match)."""
        stmt = select(Book).where(Book.author.ilike(f"%{author_name}%")).order_by(Book.title.asc())
        return list(self.session.scalars(stmt).all())


async def provide_book_repo(db_session: Session) -> BookRepository:
    """Provide book repository instance with auto-commit."""
    return BookRepository(session=db_session, auto_commit=True)
