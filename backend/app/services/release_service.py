from app.dependencies import database_dep
from app.repositories import ReleaseRepository, get_release_repository


class ReleaseService:
  def __init__(self, release_repository: ReleaseRepository):
    self.__release_repository = release_repository


def get_release_service(db: database_dep) -> ReleaseService:
  return ReleaseService(get_release_repository(db))
