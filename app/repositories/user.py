"""Repository for User database operations."""

from advanced_alchemy.repository import SQLAlchemySyncRepository
from litestar.dto import DTOData
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.models import User

password_hasher = PasswordHash.recommended()


class UserRepository(SQLAlchemySyncRepository[User]):
    """Repository for user database operations."""

    model_type = User

    def add_with_hashed_password(self, data: DTOData[User]):
        """Add user with hashed password."""
        data_dict = data.as_builtins()
        data_dict["password"] = password_hasher.hash(data_dict["password"])

        return self.add(User(**data_dict))


async def provide_user_repo(db_session: Session) -> UserRepository:
    """Provide user repository instance with auto-commit."""
    return UserRepository(session=db_session, auto_commit=True)
