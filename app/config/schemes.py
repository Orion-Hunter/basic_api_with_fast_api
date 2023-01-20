from pydantic import PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    # from: https://github.com/tiangolo/full-stack-fastapi-postgresql/pull/359/files
    allowed_schemes = {"postgres+asyncpg", "postgresql+asyncpg"}
