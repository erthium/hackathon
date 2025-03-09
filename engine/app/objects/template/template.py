from dataclasses import dataclass
from typing import List

from .command import Command


@dataclass
class Template:
  name: str
  description: str
  version: str
  author: str
  user_template_dir: str
  commands: List[Command]
