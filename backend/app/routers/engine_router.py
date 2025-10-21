import traceback
from typing import Annotated
from fastapi import APIRouter, Body

from app.dependencies.release_service import ReleaseServiceDep
from app.objects.engine import RunCommandResponse
from app.objects.message_response import MessageResponse
from app.utils import ErrorUtils

router = APIRouter(prefix="/engine")


@router.post("/result", response_model=MessageResponse)
async def on_engine_result(
  run_command_response: Annotated[RunCommandResponse, Body()],
  release_service: ReleaseServiceDep,
) -> MessageResponse:
  try:
    release_service.handle_on_submission_complete(
      run_command_response.command_run_id,
      run_command_response.scores,
      run_command_response.run_command_type,
      run_command_response.success,
      run_command_response.error,
    )
    return MessageResponse(message="Release result received successfully")
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)
