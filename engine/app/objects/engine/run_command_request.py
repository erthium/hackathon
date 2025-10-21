from uuid import UUID
from typing import List
from pydantic import BaseModel

from app.objects.enums import RunCommandType


class RunCommandRequest(BaseModel):
  command_run_id: UUID
  run_command_type: RunCommandType
  template_name: str
  command_name: str
  args: List[str]
