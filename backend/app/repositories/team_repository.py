"""
Team Repository: This repository will be used to interact with the database for the Team entity.
"""

from typing import Optional
from uuid import UUID

from app.entities import Team
from dependencies.database import DatabaseDep


class TeamRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(self, name: str) -> Team:
    team = Team(name=name)
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


def get_team_repository(db: DatabaseDep) -> TeamRepository:
  return TeamRepository(db)
