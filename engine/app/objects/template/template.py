from dataclasses import dataclass
from typing import List

from .score_metric import ScoreMetric
from .command import Command


@dataclass
class Template:
  name: str
  description: str
  version: str
  author: str
  user_template_dir: str
  commands: List[Command]
  score_metrics: List[ScoreMetric]
  on_submission_command: str = None
  on_competition_end_command: str = None
