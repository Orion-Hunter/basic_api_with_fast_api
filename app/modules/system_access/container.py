from dependency_injector import containers, providers

from .infra.sqlalchemy_uow import SqlAlchemyUnitOfWork


class SystemAccessContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    database = providers.Dependency()  # type: ignore

    uow = providers.Factory(
        SqlAlchemyUnitOfWork,
        session_factory=database.provided.session_factory,
    )
