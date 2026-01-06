"""Database models for the library management system."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import StrEnum

from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy import ForeignKey, Numeric, String, Table, Column, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Association table for many-to-many relationship between Book and Category
book_categories = Table(
    "book_categories",
    BigIntAuditBase.metadata,
    Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


class Category(BigIntAuditBase):
    """Category model."""

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(), unique=True)
    description: Mapped[str | None] = mapped_column(String(), nullable=True)

    books: Mapped[list[Book]] = relationship(  # type: ignore[name-defined]
        secondary=book_categories,
        back_populates="categories",
        lazy="selectin",
    )


class User(BigIntAuditBase):
    """User model with audit fields."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str]
    password: Mapped[str]

    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str | None] = mapped_column(nullable=True)
    address: Mapped[str | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    loans: Mapped[list[Loan]] = relationship(back_populates="user")  # type: ignore[name-defined]
    reviews: Mapped[list[Review]] = relationship(back_populates="user")  # type: ignore[name-defined]


class Book(BigIntAuditBase):
    """Book model with audit fields."""

    __tablename__ = "books"

    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    isbn: Mapped[str] = mapped_column(unique=True)
    pages: Mapped[int]
    published_year: Mapped[int]

    stock: Mapped[int] = mapped_column(default=1)
    description: Mapped[str | None] = mapped_column(nullable=True)
    language: Mapped[str | None] = mapped_column(nullable=True)
    publisher: Mapped[str | None] = mapped_column(nullable=True)

    loans: Mapped[list[Loan]] = relationship(back_populates="book")  # type: ignore[name-defined]
    categories: Mapped[list[Category]] = relationship(
        secondary=book_categories,
        back_populates="books",
        lazy="selectin",
    )
    reviews: Mapped[list[Review]] = relationship(back_populates="book", lazy="selectin")  # type: ignore[name-defined]


class LoanStatus(StrEnum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"


class Loan(BigIntAuditBase):
    """Loan model with audit fields."""

    __tablename__ = "loans"

    loan_dt: Mapped[date] = mapped_column(default=datetime.today)
    due_date: Mapped[date] = mapped_column(default=lambda: (date.today() + timedelta(days=14)))
    return_dt: Mapped[date | None]

    fine_amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[LoanStatus] = mapped_column(
        SAEnum(LoanStatus, name="loanstatus"),
        default=LoanStatus.ACTIVE,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped[User] = relationship(back_populates="loans")
    book: Mapped[Book] = relationship(back_populates="loans")


class Review(BigIntAuditBase):
    """Review model for book reviews."""

    __tablename__ = "reviews"

    rating: Mapped[int]
    comment: Mapped[str]
    review_date: Mapped[date] = mapped_column(default=date.today)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))

    user: Mapped[User] = relationship(back_populates="reviews", lazy="selectin")
    book: Mapped[Book] = relationship(back_populates="reviews", lazy="selectin")


@dataclass
class PasswordUpdate:
    """Password update request."""

    current_password: str
    new_password: str


@dataclass
class BookStats:
    """Book statistics data."""

    total_books: int
    average_pages: float
    oldest_publication_year: int | None
    newest_publication_year: int | None
