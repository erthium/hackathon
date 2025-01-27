from typing import List
from uuid import UUID

from pydantic import BaseModel


class TeamErrors(BaseModel):
  team_id: UUID
  team_name: str
  repository_creation_error: bool
  failed_member_invitations: List[str]
  webhook_creation_error: bool


class StartCompetitionResponse(BaseModel):
  competition_id: UUID
  template_repository_owner: str
  template_repository_name: str
  team_errors: List[TeamErrors]
