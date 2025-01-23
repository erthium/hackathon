from pydantic import BaseModel
from uuid import UUID


class StartCompetitionRequest(BaseModel):
  competition_id: UUID
  template_repository_owner: str
  template_repository_name: str
