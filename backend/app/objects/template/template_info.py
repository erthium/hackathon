from dataclasses import dataclass
from typing import List
from typing import Optional

from .command_info import CommandInfo
from app.entities import Template, Command


@dataclass
class TemplateInfo:
  name: str
  author: str
  commands: List[CommandInfo]
  description: Optional[str] = None

  @staticmethod
  def from_entity(template: Template) -> "TemplateInfo":
    return TemplateInfo(
      name=template.name,
      description=template.description,
      author=template.author,
      commands=[CommandInfo.from_entity(command) for command in template.commands],
    )