from typing import Annotated, List
from fastapi import Body, APIRouter, Request
import traceback

from app.utils import ErrorUtils
from app.objects.template import Template, GetAllTemplatesResponse
from app.dependencies import TemplateServiceDep


router = APIRouter(prefix="/template")


@router.get(
  "/all",
  summary="Get all templates",
  description="Get all templates",
  response_description="List of all templates",
  response_model=GetAllTemplatesResponse,
)
def get_all_templates(request: Request, template_service: TemplateServiceDep) -> GetAllTemplatesResponse:
  try:
    all_templates: List[Template] = template_service.get_all_templates()
    return GetAllTemplatesResponse(templates=all_templates)
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)
