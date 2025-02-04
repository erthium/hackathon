import datetime
from uuid import UUID

from app.objects.enums import ReleaseStatus
from pydantic import BaseModel


class ReleaseInfo(BaseModel):
  id: UUID
  team_id: UUID
  team_name: str
  commit_id: str
  status: ReleaseStatus
  message: str | None
  score: float | None
  release_date: datetime.datetime
  created_at: datetime.datetime
  updated_at: datetime.datetime

  @classmethod
  def from_entity(cls, release):
    return cls(
      id=release.id,
      team_id=release.team_id,
      team_name=release.team.name,
      commit_id=release.commit_id,
      status=release.status,
      message=release.message,
      score=release.score,
      release_date=release.release_date,
      created_at=release.created_at,
      updated_at=release.updated_at,
    )
