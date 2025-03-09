import traceback

from app.dependencies.template_service import template_service_dep
from app.objects.template import GetAllTemplatesResponse
from app.objects.message_response import MessageResponse
from app.utils import ErrorUtils
from fastapi import APIRouter, Request

router = APIRouter(
  prefix="/template",
  tags=["template"],
)


@router.get(
  "/all",
  response_model=GetAllTemplatesResponse,
)
async def get_all_templates(
  request: Request,
  template_service: template_service_dep,
) -> GetAllTemplatesResponse:
  try:
    return template_service.get_all()
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)


@router.post(
  "/sync",
  response_model=MessageResponse,
)
async def sync_templates(
  request: Request,
  template_service: template_service_dep,
) -> MessageResponse:
  try:
    template_service.sync()
    return MessageResponse(message="Templates synced successfully")
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)
