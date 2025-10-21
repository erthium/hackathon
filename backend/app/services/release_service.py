from uuid import UUID
from fastapi import HTTPException, status
from typing import List, Dict

from app.dependencies.database import DatabaseDep
from app.entities import Release, CommandRun, Score
from app.objects.enums import ReleaseStatus, RunCommandType
from app.objects.message_response import MessageResponse
from app.objects.release import GetAllResponse, ReleaseInfo
from app.objects.github.webhook_events import PushEvent
from app.repositories import (
  ReleaseRepository, get_release_repository,
  CommandRunRepository, get_command_run_repository,
  ScoreMetricRepository, get_score_metric_repository,
  ScoreRepository, get_score_repository,
)


class ReleaseService:
  def __init__(self,
               release_repository: ReleaseRepository,
               command_run_repository: CommandRunRepository,
               score_metric_repository: ScoreMetricRepository,
               score_repository: ScoreRepository,
              ):
    self.__release_repository = release_repository
    self.__command_run_repository = command_run_repository
    self.__score_metric_repository = score_metric_repository
    self.__score_repository = score_repository


  def get_all(self) -> GetAllResponse:
    all_releases = self.__release_repository.get_all()
    return GetAllResponse(
      releases=[ReleaseInfo.from_entity(release) for release in all_releases]
    )


  def create_command_run_by_push_event(self, team_id: UUID, push_event: PushEvent) -> CommandRun:
    commit_id = push_event.head_commit.id
    release_date = push_event.head_commit.timestamp
    print(f"Creating release for team {team_id} with commit {commit_id} at {release_date}")
    release = self.__release_repository.create(
      team_id=team_id,
      commit_id=commit_id,
      release_date=release_date,
    )
    command_run = self.__command_run_repository.create(
      release_id=release.id,
      run_command_type=RunCommandType.ON_SUBMISSION,
      message=None,
    )
    return command_run


  def handle_on_submission_complete(self, command_run_id: UUID, scores: Dict[str, float], run_command_type: RunCommandType, success: bool, error: str | None = None) -> Release:
    command_run = self.__command_run_repository.get_by_id(command_run_id)
    if command_run is None:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"CommandRun with ID '{command_run_id}' not found"
      )

    template_id = command_run.release.team.competition.template.id

    command_run.message = error if error else "Command run completed successfully"
    self.__command_run_repository.save(command_run)

    release = command_run.release
    release.status = ReleaseStatus.APPROVED if success else ReleaseStatus.REJECTED
    self.__release_repository.save(release)

    for score_metric_name, score_value in scores.items():
      score_metric = self.__score_metric_repository.get_by_name(template_id, score_metric_name)
      if score_metric is None:
        raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Score metric '{score_metric_name}' not found for command run {command_run_id}"
        )
      score = Score(
        score_metric_id=score_metric.id,
        command_run_id=command_run_id,
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
    get_command_run_repository(db),
    get_score_metric_repository(db),
    get_score_repository(db),
  )
