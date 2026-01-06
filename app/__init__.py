"""Main Litestar application for library management."""

from litestar.app import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin, SwaggerRenderPlugin

from app.config import settings
from app.controllers.auth import AuthController
from app.controllers.book import BookController
from app.controllers.category import CategoryController
from app.controllers.loan import LoanController
from app.controllers.review import ReviewController
from app.controllers.user import UserController
from app.db import sqlalchemy_plugin
from app.security import oauth2_auth

openapi_config = OpenAPIConfig(
    title="Mi API",
    version="0.1",
    render_plugins=[
        ScalarRenderPlugin(),
        SwaggerRenderPlugin(),
    ],
)

app = Litestar(
    route_handlers=[
        UserController,
        BookController,
        CategoryController,
        ReviewController,
        LoanController,
        AuthController,
    ],
    openapi_config=openapi_config,
    debug=settings.debug,
    plugins=[sqlalchemy_plugin],
    on_app_init=[oauth2_auth.on_app_init],
)
