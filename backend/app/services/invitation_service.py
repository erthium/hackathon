from app.entities import Invitation
from app.repositories import InvitationRepository, get_invitation_repository
from app.dependencies import database_dep


class InvitationService:
  def __init__(self, invitation_repository: InvitationRepository):
    self.__invitation_repository = invitation_repository


def get_invitation_service(db: database_dep) -> InvitationService:
  return InvitationService(get_invitation_repository(db))
