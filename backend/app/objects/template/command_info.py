from dataclasses import dataclass
from typing import List, Optional

from app.objects.enums import CommandArgType
from app.entities import Command


@dataclass
class CommandInfo:
  name: str
  arg_type: CommandArgType
  allocated_ram: int
  allocated_v_ram: int
  allocated_cpu: int
  description: Optional[str] = None
  timeout: Optional[int] = None

  @staticmethod
  def from_entity(command: Command) -> "CommandInfo":
    return CommandInfo(
      name=command.name,
      description=command.description,
      arg_type=command.arg_type,
      allocated_ram=command.allocated_ram,
      allocated_v_ram=command.allocated_v_ram,
      allocated_cpu=command.allocated_cpu,
      timeout=command.timeout,
    )