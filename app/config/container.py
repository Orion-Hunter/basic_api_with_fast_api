from dependency_injector import containers, providers

from ..database.async_database import AsyncDatabase


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()  # type: ignore

    config = providers.Configuration()

    database: providers.Provider[AsyncDatabase] = providers.Singleton(
        AsyncDatabase, db_url=config.DATABASE_URL
    )
