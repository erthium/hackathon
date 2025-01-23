from app.entities import Team
from app.repositories import TeamRepository, get_team_repository
from app.dependencies import database_dep


class TeamService:
  def __init__(self, team_repository: TeamRepository):
    self.__team_repository = team_repository


def get_team_service(db: database_dep) -> TeamService:
  return TeamService(get_team_repository(db))
