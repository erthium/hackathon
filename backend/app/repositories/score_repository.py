"""
Score Repository: This repository will be used to interact with the database for the Score entity.
"""

from typing import Optional
from uuid import UUID

from app.dependencies.database import DatabaseDep
from app.entities import Score


class ScoreRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(
    self,
    score_metric_id: UUID,
    team_id: UUID,
    value: float,
  ) -> Score:
    score = Score(
      score_metric_id=score_metric_id,
      team_id=team_id,
      value=value,
    )
    self.db.add(score)
    self.db.commit()
    self.db.refresh(score)
    return score

  def save(self, score: Score) -> Score:
    self.db.add(score)
    self.db.commit()
    self.db.refresh(score)
    return score

  def get_by_id(self, command_id: UUID) -> Optional[Score]:
    return self.db.query(Score).filter(Score.id == command_id).first()

  def delete(self, score: Score):
    self.db.delete(score)
    self.db.commit()

  def delete_all(self):
    self.db.query(Score).delete()
    self.db.commit()


def get_score_repository(db: DatabaseDep) -> ScoreRepository:
  return ScoreRepository(db)
