from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    APP_NAME: str = """Pydantic Data Modelling"""
    DEBUG: bool = Field(env="DEBUG", default=True)
    DATABASE_URL: str = Field(
        env="DATABASE_URL",
    )

    TIMEZONE: str = Field(default="America/Sao_Paulo", env="TIMEZONE")

    DOCS_URL: Optional[str] = Field(None, env="DOCS_URL")
    REDOC_URL: Optional[str] = Field(None, env="REDOC_URL")
    OPENAPI_URL: Optional[str] = Field(None, env="OPENAPI_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
