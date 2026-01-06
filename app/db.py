"""Database configuration with SQLAlchemy."""

from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin, SQLAlchemySyncConfig

from app.config import settings

sqlalchemy_config = SQLAlchemySyncConfig(connection_string=settings.database_url)

sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)
