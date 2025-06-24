from dataclasses import dataclass
from typing import List, Optional

from app.entities import ScoreMetric


@dataclass
class ScoreMetricInfo:
  name: str
  description: str
  type: str
  is_ascending: bool
  is_primary: bool
  is_public: bool
  min_value: Optional[float] = None
  max_value: Optional[float] = None

  @staticmethod
  def from_entity(score_metric: ScoreMetric) -> "ScoreMetricInfo":
    return ScoreMetricInfo(
      name=score_metric.name,
      description=score_metric.description,
      type=score_metric.type,
      is_ascending=score_metric.is_ascending,
      is_primary=score_metric.is_primary,
      is_public=score_metric.is_public,
      min_value=score_metric.min_value,
      max_value=score_metric.max_value
    )
