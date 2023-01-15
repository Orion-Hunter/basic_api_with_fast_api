# FastAPI
from fastapi import FastAPI

from app.api.controllers import index
from app.config.main import settings

app = FastAPI(
    title="Pandora Insights",
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    version="0.0.0",
)

app.include_router(
    prefix="/v1",
    tags=["Index"],
    router=index.router,
)
