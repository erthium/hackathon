from uuid import UUID

from app.dependencies.database import DatabaseDep
from app.repositories import (
  TeamRepository, get_team_repository,
  ReleaseRepository, get_release_repository,
)
from app.objects.github.webhook_events import PushEvent
from app.entities import Release, Team


class TeamService:
  def __init__(self, team_repository: TeamRepository, release_repository: ReleaseRepository):
    self.__team_repository = team_repository
    self.__release_repository = release_repository


  def get_team_by_repo(self, github_repo: str) -> Team:
    team = self.__team_repository.get_by_repo(github_repo=github_repo)
    if team is None:
      raise ValueError(f"Team with GitHub repository {github_repo} does not exist")
    return team


  def can_team_make_submission(self, team: Team) -> bool:
    dailly_submission_limit = team.competition.daily_submission_limit
    extra_submission_for_the_team = team.extra_submission_count or 0
    total_daily_limit = dailly_submission_limit + extra_submission_for_the_team
    releases_today = self.__release_repository.get_release_count_today(team.id)
    return releases_today < total_daily_limit


def get_team_service(db: DatabaseDep) -> TeamService:
  return TeamService(
    get_team_repository(db),
    get_release_repository(db)
  )
