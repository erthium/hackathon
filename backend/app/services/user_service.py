from app.dependencies.database import DatabaseDep
from app.repositories import UserRepository, get_user_repository


class UserService:
  def __init__(self, user_repository: UserRepository):
    self.__user_repository = user_repository


def get_user_service(db: DatabaseDep) -> UserService:
  return UserService(get_user_repository(db))
