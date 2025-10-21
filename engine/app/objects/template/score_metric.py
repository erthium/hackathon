from dataclasses import dataclass
from typing import Optional


@dataclass
class ScoreMetric:
  name: str
  description: str
  is_ascending: bool
  is_primary: bool
  is_public: bool
  min_value: Optional[float] = None
  max_value: Optional[float] = None
