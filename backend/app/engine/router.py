from typing import Annotated

from app.objects.engine import RunEngineResponse
from fastapi import APIRouter, Body

router = APIRouter(prefix="/engine")


@router.post("/result", response_model=RunEngineResponse)
async def on_engine_result(
  payload: Annotated[RunEngineResponse, Body()],
) -> RunEngineResponse:
  # TODO: We should do some CRUD here
  print(payload)
  return payload
