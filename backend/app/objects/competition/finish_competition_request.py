from pydantic import BaseModel
from uuid import UUID


class FinishCompetitionRequest(BaseModel):
  competition_id: UUID
