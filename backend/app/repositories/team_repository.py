"""
Team Repository: This repository will be used to interact with the database for the Team entity.
"""

from typing import List, Optional
from uuid import UUID

from app.dependencies.database import database_dep
from app.entities import Team


class TeamRepository:
  def __init__(self, db: database_dep):
    self.db = db

  def create(self, competition_id: UUID, name: str) -> Team:
    team = Team(
      competition_id=competition_id,
      name=name,
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

  def delete(self, team: Team):
    self.db.delete(team)
    self.db.commit()

  def get_all_by_competition_id(self, competition_id: UUID) -> List[Team]:
    return self.db.query(Team).filter(Team.competition_id == competition_id).all()


def get_team_repository(db: database_dep) -> TeamRepository:
  return TeamRepository(db)
