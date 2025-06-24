from typing import List, Optional
from functools import lru_cache

from app.core.settings import app_settings
from app.objects.template import Command, Template
from app.objects.enums import CommandArgType


class CommandService:
  def __init__(self):
    pass


  def _get_command(self, template: Template, command_name: str) -> Optional[Command]:
    for command in template.commands:
      if command.name == command_name:
        return command
    return False


  def _validate_command_args(self, command: Command, args: List[str]) -> bool:
    if command.arg_type == CommandArgType.SENDER_REPO:
      if len(args) != 1:
        return False
      if not isinstance(args[0], str):
        return False
    elif command.arg_type == CommandArgType.ALL_REPOS:
      if len(args) <= 1:
        return False
      for arg in args:
        if not isinstance(arg, str):
          return False
    return True


  def validate_and_get_command(self, template: Template, command_name: str, args: List[str]) -> Optional[Command]:
    command: Optional[Command] = self._get_command(template, command_name)
    if not command:
      return None

    if not self._validate_command_args(command, args):
      return None

    return command


@lru_cache
def get_command_service() -> CommandService:
  return CommandService()
