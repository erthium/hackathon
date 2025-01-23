"""
Invitation Repository: This repository will be used to interact with the database for the Invitation entity.
"""

from typing import Optional
from uuid import UUID

from app.dependencies.database import database_dep
from app.entities import Invitation


class InvitationRepository:
  def __init__(self, db: database_dep):
    self.db = db

  def create(self, team_id: UUID, github_username: str, email: str) -> Invitation:
    invitation = Invitation(
      team_id=team_id,
      github_username=github_username,
      email=email,
    )
    self.db.add(invitation)
    self.db.commit()
    self.db.refresh(invitation)
    return invitation

  def save(self, invitation: Invitation) -> Invitation:
    self.db.add(invitation)
    self.db.commit()
    self.db.refresh(invitation)
    return invitation

  def get_by_id(self, invitation_id: UUID) -> Optional[Invitation]:
    return self.db.query(Invitation).filter(Invitation.id == invitation_id).first()

  def delete(self, invitation: Invitation):
    self.db.delete(invitation)
    self.db.commit()


def get_invitation_repository(db: database_dep) -> InvitationRepository:
  return InvitationRepository(db)
