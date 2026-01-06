"""Add categories, reviews, and update core models

Revision ID: f123e25e1159
Revises: acc8ae75f9e8
Create Date: 2026-01-06

"""
from __future__ import annotations

from typing import Sequence, Union

import advanced_alchemy
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f123e25e1159"
down_revision: Union[str, Sequence[str], None] = "acc8ae75f9e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    dialect = bind.dialect.name

    # --- books ---
    op.add_column("books", sa.Column("stock", sa.Integer(), nullable=False, server_default="1"))
    op.add_column("books", sa.Column("description", sa.String(), nullable=True))
    op.add_column("books", sa.Column("language", sa.String(), nullable=True))
    op.add_column("books", sa.Column("publisher", sa.String(), nullable=True))
    op.alter_column("books", "stock", server_default=None)

    # --- categories + association table ---
    op.create_table(
        "categories",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column("updated_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_categories")),
        sa.UniqueConstraint("name", name=op.f("uq_categories_name")),
    )

    op.create_table(
        "book_categories",
        sa.Column("book_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("category_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], name=op.f("fk_book_categories_book_id_books"), ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], name=op.f("fk_book_categories_category_id_categories"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("book_id", "category_id", name=op.f("pk_book_categories")),
    )
    op.create_index(op.f("ix_book_categories_book_id"), "book_categories", ["book_id"])
    op.create_index(op.f("ix_book_categories_category_id"), "book_categories", ["category_id"])

    # --- users ---
    op.add_column("users", sa.Column("email", sa.String(), nullable=False))
    op.add_column("users", sa.Column("phone", sa.String(), nullable=True))
    op.add_column("users", sa.Column("address", sa.String(), nullable=True))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.create_unique_constraint(op.f("uq_users_email"), "users", ["email"])
    op.alter_column("users", "is_active", server_default=None)

    # For existing rows, populate a placeholder email if needed (avoid nulls)
    op.execute("UPDATE users SET email = username || '@example.com' WHERE email IS NULL OR email = ''")

    # --- loan status enum ---
    loan_status_enum = sa.Enum("ACTIVE", "RETURNED", "OVERDUE", name="loanstatus")
    if dialect != "sqlite":
        loan_status_enum.create(bind, checkfirst=True)

    # --- loans ---
    op.add_column("loans", sa.Column("due_date", sa.Date(), nullable=True))
    op.add_column("loans", sa.Column("fine_amount", sa.Numeric(10, 2), nullable=True))
    op.add_column("loans", sa.Column("status", loan_status_enum, nullable=False, server_default="ACTIVE"))

    # Set due_date for existing rows: loan_dt + 14 days
    if dialect == "sqlite":
        op.execute("UPDATE loans SET due_date = date(loan_dt, '+14 day') WHERE due_date IS NULL")
    else:
        op.execute("UPDATE loans SET due_date = loan_dt + INTERVAL '14 day' WHERE due_date IS NULL")

    op.alter_column("loans", "due_date", nullable=False)
    op.alter_column("loans", "status", server_default=None)

    # --- reviews ---
    op.create_table(
        "reviews",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.String(), nullable=False),
        sa.Column("review_date", sa.Date(), nullable=False),
        sa.Column("user_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("book_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("created_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.Column("updated_at", advanced_alchemy.types.datetime.DateTimeUTC(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"], name=op.f("fk_reviews_book_id_books")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_reviews_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_reviews")),
    )
    op.create_index(op.f("ix_reviews_book_id"), "reviews", ["book_id"])
    op.create_index(op.f("ix_reviews_user_id"), "reviews", ["user_id"])


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    dialect = bind.dialect.name

    op.drop_index(op.f("ix_reviews_user_id"), table_name="reviews")
    op.drop_index(op.f("ix_reviews_book_id"), table_name="reviews")
    op.drop_table("reviews")

    op.drop_column("loans", "status")
    op.drop_column("loans", "fine_amount")
    op.drop_column("loans", "due_date")

    loan_status_enum = sa.Enum("ACTIVE", "RETURNED", "OVERDUE", name="loanstatus")
    if dialect != "sqlite":
        loan_status_enum.drop(bind, checkfirst=True)

    op.drop_constraint(op.f("uq_users_email"), "users", type_="unique")
    op.drop_column("users", "is_active")
    op.drop_column("users", "address")
    op.drop_column("users", "phone")
    op.drop_column("users", "email")

    op.drop_index(op.f("ix_book_categories_category_id"), table_name="book_categories")
    op.drop_index(op.f("ix_book_categories_book_id"), table_name="book_categories")
    op.drop_table("book_categories")
    op.drop_table("categories")

    op.drop_column("books", "publisher")
    op.drop_column("books", "language")
    op.drop_column("books", "description")
    op.drop_column("books", "stock")
