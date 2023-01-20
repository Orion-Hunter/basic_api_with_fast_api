from dependency_injector import containers, providers

from ..database.async_database import AsyncDatabase
from ..modules.system_access import SystemAccessContainer


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()  # type: ignore

    config = providers.Configuration()

    database: providers.Provider[AsyncDatabase] = providers.Singleton(
        AsyncDatabase, db_url=config.DATABASE_URL
    )

    systemaccess = providers.Container(
        SystemAccessContainer,
        database=database,
    )
