import datetime
from uuid import UUID

from app.dependencies import database_dep
from app.entities import Release
from app.objects.enums import ReleaseStatus
from app.objects.message_response import MessageResponse
from app.objects.release import GetAllResponse, ReleaseInfo
from app.repositories import ReleaseRepository, get_release_repository


class ReleaseService:
  def __init__(self, release_repository: ReleaseRepository):
    self.__release_repository = release_repository

  def get_all(self) -> GetAllResponse:
    all_releases = self.__release_repository.get_all()
    return GetAllResponse(
      releases=[ReleaseInfo.from_entity(release) for release in all_releases]
    )

  def create(
    self, team_id: UUID, commit_id: str, release_date: datetime.datetime
  ) -> Release:
    return self.__release_repository.create(team_id, commit_id, release_date)

  def update(
    self,
    release_id: UUID,
    status: ReleaseStatus,
    score: float | None = None,
    message: str | None = None,
  ) -> MessageResponse:
    release = self.__release_repository.get_by_id(release_id)

    if release is None:
      return MessageResponse(message=f"Release {release_id} not found")

    release.status = status
    release.score = score
    release.message = message
    self.__release_repository.save(release)

    return MessageResponse(message=f"Release {release_id} updated")


def get_release_service(db: database_dep) -> ReleaseService:
  return ReleaseService(get_release_repository(db))
