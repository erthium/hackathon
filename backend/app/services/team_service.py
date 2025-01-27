from app.dependencies import database_dep
from app.entities.team import Team
from app.repositories import TeamRepository, get_team_repository


class TeamService:
  def __init__(self, team_repository: TeamRepository):
    self.__team_repository = team_repository

  def get_by_github_repo(self, repo_name: str) -> Team | None:
    return self.__team_repository.get_by_github_repo(repo_name)


def get_team_service(db: database_dep) -> TeamService:
  return TeamService(get_team_repository(db))
