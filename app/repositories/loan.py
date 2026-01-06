"""Repository for Loan database operations."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Sequence

from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models import Book, Loan, LoanStatus


FINE_PER_DAY = Decimal("5000")


class LoanRepository(SQLAlchemySyncRepository[Loan]):
    """Repository for loan database operations."""

    model_type = Loan

    def get_active_loans(self, user_id: int) -> Sequence[Loan]:
        """Return active loans for a user."""
        stmt = (
            select(Loan)
            .where(Loan.user_id == user_id)
            .where(Loan.status == LoanStatus.ACTIVE)
            .order_by(Loan.loan_dt.desc())
        )
        return list(self.session.scalars(stmt).all())

    def get_overdue_loans(self) -> Sequence[Loan]:
        """Return overdue loans and mark ACTIVE loans as OVERDUE if due_date has passed."""
        today = date.today()

        # Mark ACTIVE loans as OVERDUE where due_date < today
        self.session.execute(
            update(Loan)
            .where(Loan.status == LoanStatus.ACTIVE)
            .where(Loan.due_date < today)
            .values(status=LoanStatus.OVERDUE)
        )
        self.session.commit()

        stmt = select(Loan).where(Loan.status == LoanStatus.OVERDUE).order_by(Loan.due_date.asc())
        return list(self.session.scalars(stmt).all())

    def calculate_fine(self, loan: Loan) -> Decimal:
        """Calculate fine based on days overdue."""
        if loan.due_date is None:
            return Decimal("0")
        end_dt = loan.return_dt or date.today()
        days = (end_dt - loan.due_date).days
        if days <= 0:
            return Decimal("0")
        return FINE_PER_DAY * Decimal(days)

    def return_book(self, loan_id: int) -> Loan:
        """Process book return: set return_dt, status, and fine_amount."""
        loan = self.get(loan_id)
        if loan.status == LoanStatus.RETURNED:
            return loan

        loan.return_dt = date.today()

        fine = self.calculate_fine(loan)
        loan.fine_amount = fine if fine > 0 else None
        loan.status = LoanStatus.RETURNED

        # Increment book stock
        book = self.session.get(Book, loan.book_id)
        if book is not None:
            book.stock = (book.stock or 0) + 1
            self.session.add(book)

        self.session.add(loan)
        self.session.commit()
        return loan

    def get_user_loan_history(self, user_id: int) -> Sequence[Loan]:
        """Return full loan history for a user ordered by loan date."""
        stmt = select(Loan).where(Loan.user_id == user_id).order_by(Loan.loan_dt.desc())
        return list(self.session.scalars(stmt).all())


async def provide_loan_repo(db_session: Session) -> LoanRepository:
    """Provide loan repository instance with auto-commit."""
    return LoanRepository(session=db_session, auto_commit=True)
