from uuid import UUID
from fastapi import HTTPException, status
from typing import List

from app.dependencies.database import DatabaseDep
from app.entities import Release, Score
from app.objects.enums import ReleaseStatus, RunCommandType
from app.objects.message_response import MessageResponse
from app.objects.release import GetAllResponse, ReleaseInfo
from app.objects.github.webhook_events import PushEvent
from app.repositories import (
  ReleaseRepository, get_release_repository,
  ScoreRepository, get_score_repository,
)


class ReleaseService:
  def __init__(self,
               release_repository: ReleaseRepository,
               score_repository: ScoreRepository,
              ):
    self.__release_repository = release_repository
    self.__score_repository = score_repository


  def get_all(self) -> GetAllResponse:
    all_releases = self.__release_repository.get_all()
    return GetAllResponse(
      releases=[ReleaseInfo.from_entity(release) for release in all_releases]
    )


  def create_by_push_event(self, team_id: UUID, push_event: PushEvent) -> Release:
    commit_id = push_event.head_commit.id
    release_date = push_event.head_commit.timestamp
    print(f"Creating release for team {team_id} with commit {commit_id} at {release_date}")
    release = self.__release_repository.create(
      team_id=team_id,
      commit_id=commit_id,
      release_date=release_date,
    )
    return release


  def handle_on_submission_complete(self, release_id: UUID, scores: List[float], run_command_type: RunCommandType, success: bool, error: str | None = None) -> Release:
    release = self.__release_repository.get_by_id(release_id)

    if release is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Release with ID '{release_id}' not found"
      )

    release.status = ReleaseStatus.APPROVED if success else ReleaseStatus.REJECTED
    release.message = error if error else "Release processed successfully"
    self.__release_repository.save(release)

    for score_value in scores:
      score = Score(
        release_id=release.id,
        value=score_value,
        run_command_type=run_command_type,
      )
      self.__score_repository.save(score)

    return release


  def update(
    self,
    release_id: UUID,
    status: ReleaseStatus | None = None,
    message: str | None = None,
  ) -> MessageResponse:
    release = self.__release_repository.get_by_id(release_id)

    if release is None:
      return MessageResponse(message=f"Release {release_id} not found")

    if status is not None:
      release.status = status
    if message is not None:
      release.message = message
    self.__release_repository.save(release)

    return MessageResponse(message=f"Release {release_id} updated")


def get_release_service(db: DatabaseDep) -> ReleaseService:
  return ReleaseService(
    get_release_repository(db),
    get_score_repository(db),
  )
