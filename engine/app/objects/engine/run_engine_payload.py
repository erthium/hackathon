import uuid
from typing import List
from pydantic import BaseModel


class RunEnginePayload(BaseModel):
  id: uuid.UUID  # Database ID type
  """
  repo_owner: str
  repo_name: str
  commit_id: str
  """
  template_name: str
  command: str
  args: List[str]
