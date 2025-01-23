from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class NecessaryUserInfo(BaseModel):
  email: str
  github_username: str
  username: Optional[str] = None
  name: Optional[str] = None


class NecessaryTeamInfo(BaseModel):
  name: str
  members: List[NecessaryUserInfo]


class AddTeamsRequest(BaseModel):
  competition_id: UUID
  teams: List[NecessaryTeamInfo]
