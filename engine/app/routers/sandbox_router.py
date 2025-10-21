import traceback
from typing import Annotated
from fastapi import APIRouter, Body

from app.objects.engine import CommandResult, CommandFailResult, CommandSuccessResult
from app.objects.message_response import MessageResponse
from app.utils import ErrorUtils

router = APIRouter(prefix="/sandbox")


@router.post("/result", response_model=MessageResponse)
async def on_engine_result(
  command_result: Annotated[CommandResult, Body()],
) -> MessageResponse:
  try:
    
    return MessageResponse(message="Command result received successfully")
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)
