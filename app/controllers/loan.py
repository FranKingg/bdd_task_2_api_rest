"""Controller for Loan endpoints."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Sequence

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException

from app.controllers import duplicate_error_handler, not_found_error_handler
from app.dtos.loan import LoanCreateDTO, LoanReadDTO, LoanUpdateDTO
from app.models import Book, Loan, LoanStatus
from app.repositories.book import BookRepository, provide_book_repo
from app.repositories.loan import LoanRepository, provide_loan_repo


class LoanController(Controller):
    """Controller for loan management operations."""

    path = "/loans"
    tags = ["loans"]
    return_dto = LoanReadDTO
    dependencies = {
        "loans_repo": Provide(provide_loan_repo),
        "books_repo": Provide(provide_book_repo),
    }
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_loans(self, loans_repo: LoanRepository) -> Sequence[Loan]:
        return loans_repo.list()

    @get("/{id:int}")
    async def get_loan(self, id: int, loans_repo: LoanRepository) -> Loan:
        return loans_repo.get(id)

    @post("/", dto=LoanCreateDTO)
    async def create_loan(
        self,
        data: DTOData[Loan],
        loans_repo: LoanRepository,
        books_repo: BookRepository,
    ) -> Loan:
        """Create a new loan. Sets due_date = loan_dt + 14 days and decrements book stock."""
        payload = data.as_builtins()

        book_id = int(payload["book_id"])
        book: Book = books_repo.get(book_id)

        if (book.stock or 0) <= 0:
            raise HTTPException(status_code=400, detail="No hay stock disponible para este libro")

        # Build loan instance manually to enforce due_date/status
        loan_dt = payload.get("loan_dt") or date.today()
        if isinstance(loan_dt, str):
            loan_dt = date.fromisoformat(loan_dt)

        loan = Loan(
            user_id=int(payload["user_id"]),
            book_id=book_id,
            loan_dt=loan_dt,
            due_date=loan_dt + timedelta(days=14),
            status=LoanStatus.ACTIVE,
            fine_amount=None,
            return_dt=None,
        )

        # decrement stock
        book.stock = (book.stock or 0) - 1
        books_repo.update(book)

        return loans_repo.add(loan)

    @patch("/{id:int}", dto=LoanUpdateDTO)
    async def update_loan(self, id: int, data: DTOData[Loan], loans_repo: LoanRepository) -> Loan:
        payload = data.as_builtins()

        # Only status is allowed by DTO, but we still validate values
        if "status" in payload and payload["status"] is not None:
            try:
                LoanStatus(str(payload["status"]))
            except ValueError as e:
                raise HTTPException(status_code=400, detail="status inválido") from e

        loan, _ = loans_repo.get_and_update(match_fields="id", id=id, **payload)
        return loan

    @delete("/{id:int}")
    async def delete_loan(self, id: int, loans_repo: LoanRepository) -> None:
        loans_repo.delete(id)

    # ---- Métodos requeridos por la tarea (LoanRepository + endpoints) ----

    @get("/active/{user_id:int}")
    async def get_active_loans(self, user_id: int, loans_repo: LoanRepository) -> Sequence[Loan]:
        return loans_repo.get_active_loans(user_id=user_id)

    @get("/overdue")
    async def get_overdue_loans(self, loans_repo: LoanRepository) -> Sequence[Loan]:
        return loans_repo.get_overdue_loans()

    @post("/{loan_id:int}/return")
    async def return_book(self, loan_id: int, loans_repo: LoanRepository) -> Loan:
        return loans_repo.return_book(loan_id=loan_id)

    @get("/user/{user_id:int}/history")
    async def get_user_loan_history(self, user_id: int, loans_repo: LoanRepository) -> Sequence[Loan]:
        return loans_repo.get_user_loan_history(user_id=user_id)
