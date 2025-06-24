"""
Competition Repository: This repository will be used to interact with the database for the Competition entity.
"""

import datetime
from typing import Optional, Dict
from uuid import UUID

from app.dependencies.database import DatabaseDep
from app.entities import Competition


class CompetitionRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(
    self, name: str, start_date: Optional[datetime.datetime] = None, end_date: Optional[datetime.datetime] = None
  ) -> Competition:
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

  def get_all(self) -> list[Competition]:
    return self.db.query(Competition).all()

  def get_all_with_template_names(self) -> Dict[UUID, str]:
    competitions = self.db.query(Competition.id, Competition.template_name).all()
    return {competition_id: template_name for competition_id, template_name in competitions}

  def nullify_all_template_names(self):
    self.db.query(Competition).update({Competition.template_name: None})
    self.db.commit()

  def bring_back_template_names(self, template_names: Dict[UUID, str]):
    for competition_id, template_name in template_names.items():
      self.db.query(Competition).filter(Competition.id == competition_id).update({Competition.template_name: template_name})
    self.db.commit()

def get_competition_repository(db: DatabaseDep) -> CompetitionRepository:
  return CompetitionRepository(db)
