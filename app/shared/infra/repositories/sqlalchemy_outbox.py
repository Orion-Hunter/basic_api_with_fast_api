"""
NOTE: foi dividido o outbox em dois, visto que o Local deve ficar na unidade de trabalho
do contexto, pois o mesmo deve ser executado na mesma transação da operação sendo reali-
zada naquele contexto.

Já o global, serve para o agendador de tarefas utiliza-lo para empurrar os eventos
para a fila.
"""
import json
from datetime import datetime
from typing import Callable, List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import models
from app.shared.domain.domain_events import DomainEvent
from app.shared.domain.outbox_message import OutboxMessage
from app.shared.domain.outbox_repository import OutboxRepo


class SqlAlchemyOutboxLocalRepo(OutboxRepo):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    async def insert(self, domain_events: List[DomainEvent]) -> None:
        db_events = []
        for domain_event in domain_events:
            db_event = models.shared.OutboxMessage(
                id=domain_event.id,
                aggregate_type=domain_event.aggregate_type,
                aggregate_id=domain_event.aggregate_id,
                type=type(domain_event).__name__,
                payload=json.loads(domain_event.json()),
                occurred_on=domain_event.occurred_on,
                published_on=None,
            )
            db_events.append(db_event)
        self._session.add_all(db_events)
        await self._session.flush()

    async def get_not_sended(
        self,
    ) -> List[OutboxMessage]:
        raise NotImplementedError()

    async def set_as_sended(self, outbox_message: OutboxMessage) -> None:
        raise NotImplementedError()


class SqlAlchemyOutboxGlobalRepo(OutboxRepo):
    def __init__(self, session_factory: Callable[..., AsyncSession]):
        super().__init__()
        self._session_factory = session_factory

    async def get_not_sended(
        self,
    ) -> List[OutboxMessage]:
        stmt = (
            select(
                models.shared.OutboxMessage.id,
                models.shared.OutboxMessage.aggregate_type,
                models.shared.OutboxMessage.aggregate_id,
                models.shared.OutboxMessage.type,
                models.shared.OutboxMessage.payload,
                models.shared.OutboxMessage.occurred_on,
                models.shared.OutboxMessage.published_on,
            )
            .select_from(models.shared.OutboxMessage)
            .where(models.shared.OutboxMessage.published_on == None)  # noqa
        )

        async with self._session_factory() as session:
            result = await session.execute(stmt)
        rows = result.fetchall()

        return [
            OutboxMessage(
                id=row.id,
                aggregate_type=row.aggregate_type,
                aggregate_id=row.aggregate_id,
                type=row.type,
                payload=row.payload,
                occurred_on=row.occurred_on,
                published_on=row.published_on,
            )
            for row in rows
        ]

    async def set_as_sended(self, outbox_message: OutboxMessage) -> None:
        stmt = (
            update(models.shared.OutboxMessage)
            .values(
                published_on=datetime.now(),
            )
            .where(
                models.shared.OutboxMessage.id == str(outbox_message.id),
            )
        )
        async with self._session_factory() as session:
            await session.execute(stmt)
            await session.commit()

    async def insert(self, domain_events: List[DomainEvent]) -> None:
        raise NotImplementedError()
