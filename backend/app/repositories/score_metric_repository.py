"""
ScoreMetric Repository: This repository will be used to interact with the database for the ScoreMetric entity.
"""

from typing import Optional
from uuid import UUID

from app.dependencies.database import DatabaseDep
from app.entities import ScoreMetric


class ScoreMetricRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(
    self,
    template_id: UUID,
    name: str,
    description: str,
    is_ascending: bool,
    is_primary: bool,
    is_public: bool,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
  ) -> ScoreMetric:
    score_metric = ScoreMetric(
      template_id=template_id,
      name=name,
      description=description,
      is_ascending=is_ascending,
      is_primary=is_primary,
      is_public=is_public,
      min_value=min_value,
      max_value=max_value
    )
    self.db.add(score_metric)
    self.db.commit()
    self.db.refresh(score_metric)
    return score_metric

  def save(self, score_metric: ScoreMetric) -> ScoreMetric:
    self.db.add(score_metric)
    self.db.commit()
    self.db.refresh(score_metric)
    return score_metric

  def get_by_id(self, command_id: UUID) -> Optional[ScoreMetric]:
    return self.db.query(ScoreMetric).filter(ScoreMetric.id == command_id).first()

  def delete(self, score_metric: ScoreMetric):
    self.db.delete(score_metric)
    self.db.commit()

  def delete_all(self):
    self.db.query(ScoreMetric).delete()
    self.db.commit()


def get_score_metric_repository(db: DatabaseDep) -> ScoreMetricRepository:
  return ScoreMetricRepository(db)
