from typing import Annotated

from fastapi import APIRouter, Body

from common.schemas import RunEngineResponse

router = APIRouter(prefix="/engine")


@router.post("/result", response_model=RunEngineResponse)
async def on_engine_result(
  payload: Annotated[RunEngineResponse, Body()],
) -> RunEngineResponse:
  # TODO: We should do some CRUD here
  print(payload)
  return payload
