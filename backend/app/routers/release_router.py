import traceback

from app.dependencies.release_service import release_service_dep
from app.entities.release import Release
from app.utils import ErrorUtils
from fastapi import APIRouter, Request

router = APIRouter(
  prefix="/release",
  tags=["release"],
)


@router.get("/all")
async def get_all_releases(
  request: Request, release_service: release_service_dep
) -> list[Release]:
  try:
    return release_service.get_all()
  except Exception as exception:
    traceback.print_exc()
    raise ErrorUtils.toHTTPException(exception)
