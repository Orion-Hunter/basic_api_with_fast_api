import logging
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.shared.domain import LogLevels


class AsyncDatabase:
    def __init__(self, db_url: str) -> None:

        logging.log(LogLevels.INFO, "Database Initializing...")
        self._engine = create_async_engine(
            db_url,
            echo=False,
            pool_size=10,
            max_overflow=0,
            pool_pre_ping=True,
        )
        self._session_factory = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        logging.log(LogLevels.INFO, "Database Initialized...")

    @property
    def session_factory(
        self,
    ) -> Callable[..., AsyncSession]:
        return self._session_factory

    @property
    def engine(self) -> AsyncEngine:
        return self._engine
