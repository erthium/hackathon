from typing import Annotated

from app.dependencies.release_service import release_service_dep
from app.objects.engine import RunEngineResponse
from app.objects.enums import ReleaseStatus
from app.objects.message_response import MessageResponse
from fastapi import APIRouter, Body

router = APIRouter(prefix="/engine")


@router.post("/result", response_model=MessageResponse)
async def on_engine_result(
  payload: Annotated[RunEngineResponse, Body()],
  release_service: release_service_dep,
) -> MessageResponse:
  return release_service.update(
    payload.id,
    ReleaseStatus.APPROVED if payload.data.success else ReleaseStatus.REJECTED,
  )
