"""
Team Repository: This repository will be used to interact with the database for the Team entity.
"""

from typing import List, Optional
from uuid import UUID

from app.dependencies.database import database_dep
from app.entities import Competition, Team


class TeamRepository:
  def __init__(self, db: database_dep):
    self.db = db

  def create(self, competition_id: UUID, name: str) -> Team:
    competition = (
      self.db.query(Competition).filter(Competition.id == competition_id).first()
    )

    if competition is None:
      raise ValueError(f"Competition with id {competition_id} does not exist")

    team = Team(
      competition_id=competition_id,
      name=name,
      github_repo=f"{competition.name}-{name}",
    )
    self.db.add(team)
    self.db.commit()
    self.db.refresh(team)
    return team

  def save(self, team: Team) -> Team:
    self.db.add(team)
    self.db.commit()
    self.db.refresh(team)
    return team

  def get_by_id(self, team_id: UUID) -> Optional[Team]:
    return self.db.query(Team).filter(Team.id == team_id).first()

  def get_by_github_repo(self, github_repo: str) -> Optional[Team]:
    return self.db.query(Team).filter(Team.github_repo == github_repo).first()

  def delete(self, team: Team):
    self.db.delete(team)
    self.db.commit()

  def get_all_by_competition_id(self, competition_id: UUID) -> List[Team]:
    return self.db.query(Team).filter(Team.competition_id == competition_id).all()


def get_team_repository(db: database_dep) -> TeamRepository:
  return TeamRepository(db)
