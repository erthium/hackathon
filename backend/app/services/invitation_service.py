from app.dependencies.database import DatabaseDep
from app.repositories import InvitationRepository, get_invitation_repository


class InvitationService:
  def __init__(self, invitation_repository: InvitationRepository):
    self.__invitation_repository = invitation_repository


def get_invitation_service(db: DatabaseDep) -> InvitationService:
  return InvitationService(get_invitation_repository(db))
