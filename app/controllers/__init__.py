"""Controllers and error handlers for API endpoints."""

from typing import Any

from advanced_alchemy.exceptions import DuplicateKeyError, NotFoundError
from litestar import Request, Response


def not_found_error_handler(_: Request[Any, Any, Any], __: NotFoundError) -> Response[Any]:
    """Handle not found errors."""
    return Response(
        status_code=404,
        content={"status_code": 404, "detail": "Not found"},
    )


def duplicate_error_handler(_: Request[Any, Any, Any], __: DuplicateKeyError) -> Response[Any]:
    """Handle duplicate errors."""
    return Response(
        status_code=404,
        content={"status_code": 404, "detail": "Already exists"},
    )
