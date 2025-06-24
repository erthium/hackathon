from pydantic import BaseModel
from uuid import UUID

from app.objects.enums import CompetitionStatus
from app.entities.competition import Competition


class CompetitionInfo(BaseModel):
  id: UUID
  name: str
  status: CompetitionStatus

  @classmethod
  def from_entity(cls, entity: Competition) -> "CompetitionInfo":
    return cls(
      id=entity.id,
      name=entity.name,
      status=entity.status,
    )
