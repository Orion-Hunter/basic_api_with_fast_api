from typing import Any, Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.abstract_uow import AbstractUnitOfWork
from .repositories import (
    SqlAlchemyEmployeeRepo,
    SqlAlchemyParentCompanyRepo,
    SqlAlchemySubsidiaryCompanyRepo,
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory: Callable[..., AsyncSession],
    ):
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None

    async def __aenter__(self) -> "AbstractUnitOfWork":
        async with self._session_factory() as session:
            self._session = session
            self.parent_repo = SqlAlchemyParentCompanyRepo(session=session)
            self.subsidiary_repo = SqlAlchemySubsidiaryCompanyRepo(session=session)
            self.employee_repo = SqlAlchemyEmployeeRepo(session=session)

            return await super().__aenter__()

    async def __aexit__(self, *args: Any) -> None:
        await super().__aexit__(*args)
        if not self._session:
            return None

        await self._session.close()

    async def _commit(self) -> None:
        if not self._session:
            return None

        await self._session.commit()

    async def rollback(self) -> None:
        if not self._session:
            return None

        await self._session.rollback()
