from pydantic import BaseModel
from uuid import UUID


class CreateCompetitionResponse(BaseModel):
  competitions_id: UUID
