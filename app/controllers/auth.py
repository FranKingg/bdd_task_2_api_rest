"""Controller for authentication endpoints."""

from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError

from litestar import Controller, Response, post
from litestar.di import Provide
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.security.jwt import OAuth2Login

from app.dtos.user import UserLoginDTO
from app.models import User
from app.repositories.user import UserRepository, provide_user_repo
from app.security import oauth2_auth

# Argon2 hasher (compatible con hashes $argon2id$... del initial_data.sql)
ph = PasswordHasher()


class AuthController(Controller):
    """Controller for authentication operations."""

    path = "/auth"
    tags = ["auth"]

    @post(
        "/login",
        dependencies={"users_repo": Provide(provide_user_repo)},
        dto=UserLoginDTO,
    )
    async def login(
        self,
        data: Annotated[User, Body(media_type=RequestEncodingType.URL_ENCODED)],
        users_repo: UserRepository,
    ) -> Response[OAuth2Login]:
        """Authenticate user and generate OAuth2 token."""
        user = users_repo.get_one_or_none(username=data.username)

        if user is None:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

        try:
            # verify(hashed_password, plain_password)
            ph.verify(user.password, data.password)
        except (VerifyMismatchError, InvalidHash):
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

        return oauth2_auth.login(identifier=user.username)
