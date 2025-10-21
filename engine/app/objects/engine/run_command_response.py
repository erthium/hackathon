from uuid import UUID
from typing import List, Dict, Optional
from pydantic import BaseModel

from app.objects.enums import RunCommandType


class RunCommandResponse(BaseModel):
  command_run_id: UUID
  run_command_type: RunCommandType
  template_name: str
  command_name: str
  success: bool
  scores: Dict[str, float] = {}
  warnings: List[str] = []
  error: Optional[str] = None
