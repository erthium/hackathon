import traceback

from app.dependencies.release_service import ReleaseServiceDep
from app.objects.release import GetAllResponse
from app.utils import ErrorUtils
from fastapi import APIRouter, Request

router = APIRouter(
  prefix="/release",
  tags=["release"],
)


@router.get(
  "/all",
  response_model=GetAllResponse,
)
async def get_all_releases(
  request: Request,
  release_service: ReleaseServiceDep,
) -> GetAllResponse:
  try:
    return release_service.get_all()
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)
