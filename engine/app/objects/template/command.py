from dataclasses import dataclass
from typing import List, Optional

from app.objects.enums import CommandArgType


@dataclass
class Command:
  name: str
  description: str
  usage: str
  execute: str
  arg_type: CommandArgType
  allocated_ram: int
  allocated_v_ram: int
  allocated_cpu: int
  timeout: Optional[int] = None
