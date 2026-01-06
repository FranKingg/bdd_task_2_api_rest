"""Repository for Review database operations."""

from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy.orm import Session

from app.models import Review


class ReviewRepository(SQLAlchemySyncRepository[Review]):
    """Repository for review database operations."""

    model_type = Review


async def provide_review_repo(db_session: Session) -> ReviewRepository:
    """Provide review repository instance with auto-commit."""
    return ReviewRepository(session=db_session, auto_commit=True)
