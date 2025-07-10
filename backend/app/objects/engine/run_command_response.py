from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel

from app.objects.enums import RunCommandType


class RunCommandResponse(BaseModel):
  submission_id: UUID
  run_command_type: RunCommandType
  template_name: str
  command_name: str
  success: bool
  scores: List[float] = []
  warnings: List[str] = []
  error: Optional[str] = None
