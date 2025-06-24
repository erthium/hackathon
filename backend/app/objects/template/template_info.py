from dataclasses import dataclass
from typing import List
from typing import Optional

from .command_info import CommandInfo
from .score_metric_info import ScoreMetricInfo
from app.entities import Template, Command, ScoreMetric


@dataclass
class TemplateInfo:
  name: str
  author: str
  commands: List[CommandInfo]
  score_metrics: List[ScoreMetricInfo]
  on_submission_command: Optional[str] = None
  on_competition_end_command: Optional[str] = None
  description: Optional[str] = None

  @staticmethod
  def from_entity(template: Template) -> "TemplateInfo":
    return TemplateInfo(
      name=template.name,
      description=template.description,
      author=template.author,
      commands=[CommandInfo.from_entity(command) for command in template.commands],
      score_metrics=[ScoreMetricInfo.from_entity(score_metric) for score_metric in template.score_metrics],
      on_submission_command=template.on_submission_command,
      on_competition_end_command=template.on_competition_end_command,
    )