"""Controller for Review endpoints."""

from datetime import date
from typing import Sequence

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.exceptions import HTTPException

from app.controllers import duplicate_error_handler, not_found_error_handler
from app.dtos.review import ReviewCreateDTO, ReviewReadDTO, ReviewUpdateDTO
from app.models import Review
from app.repositories.review import ReviewRepository, provide_review_repo


class ReviewController(Controller):
    """Controller for review CRUD operations."""

    path = "/reviews"
    tags = ["reviews"]
    return_dto = ReviewReadDTO
    dependencies = {"reviews_repo": Provide(provide_review_repo)}
    exception_handlers = {
        NotFoundError: not_found_error_handler,
        DuplicateKeyError: duplicate_error_handler,
    }

    @get("/")
    async def list_reviews(self, reviews_repo: ReviewRepository) -> Sequence[Review]:
        return reviews_repo.list()

    @get("/{id:int}")
    async def get_review(self, id: int, reviews_repo: ReviewRepository) -> Review:
        return reviews_repo.get(id)

    @post("/", dto=ReviewCreateDTO)
    async def create_review(self, data: DTOData[Review], reviews_repo: ReviewRepository) -> Review:
        built = data.as_builtins()
        rating = built.get("rating")
        if rating is None or not (1 <= int(rating) <= 5):
            raise HTTPException(status_code=400, detail="rating debe estar en el rango 1 a 5")

        # ensure review_date has a default (DTO might omit it)
        if built.get("review_date") is None:
            built["review_date"] = date.today()

        return reviews_repo.add(Review(**built))

    @patch("/{id:int}", dto=ReviewUpdateDTO)
    async def update_review(self, id: int, data: DTOData[Review], reviews_repo: ReviewRepository) -> Review:
        built = data.as_builtins()
        if "rating" in built and built["rating"] is not None:
            if not (1 <= int(built["rating"]) <= 5):
                raise HTTPException(status_code=400, detail="rating debe estar en el rango 1 a 5")

        review, _ = reviews_repo.get_and_update(match_fields="id", id=id, **built)
        return review

    @delete("/{id:int}")
    async def delete_review(self, id: int, reviews_repo: ReviewRepository) -> None:
        reviews_repo.delete(id)
