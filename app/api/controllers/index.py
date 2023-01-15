from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def index() -> Any:
    return {"API": "Teste", "VERSION": "1.0.0"}
