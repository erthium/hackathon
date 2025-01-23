from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class NecessaryUserInfo(BaseModel):
  email: str
  github_username: str
  username: Optional[str]
  name: Optional[str]


class NecessaryTeamInfo(BaseModel):
  name: str
  members: List[NecessaryUserInfo]


class AddTeamsRequest(BaseModel):
  competition_id: UUID
  teams: List[NecessaryTeamInfo]
