"""
Competition Repository: This repository will be used to interact with the database for the Competition entity.
"""

from typing import Optional
from uuid import UUID

from app.entities import Competition
from dependencies.database import DatabaseDep


class CompetitionRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(self, name: str, start_date: str, end_date: str) -> Competition:
    competition = Competition(
      name=name,
      start_date=start_date,
      end_date=end_date,
    )
    self.db.add(competition)
    self.db.commit()
    self.db.refresh(competition)
    return competition

  def save(self, competition: Competition) -> Competition:
    self.db.add(competition)
    self.db.commit()
    self.db.refresh(competition)
    return competition

  def get_by_id(self, competition_id: UUID) -> Optional[Competition]:
    return self.db.query(Competition).filter(Competition.id == competition_id).first()

  def delete(self, competition: Competition):
    self.db.delete(competition)
    self.db.commit()


def get_competition_repository(db: DatabaseDep) -> CompetitionRepository:
  return CompetitionRepository(db)
