from pydantic import BaseModel
from uuid import UUID

from app.objects.enums import CompetitionStatus


class CompetitionInfo(BaseModel):
  id: UUID
  name: str
  status: CompetitionStatus

  @classmethod
  def from_entity(cls, entity):
    return cls(
      id=entity.id,
      name=entity.name,
      status=entity.status,
    )
