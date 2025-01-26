"""
User Repository: This repository will be used to interact with the database for the User entity.
"""

from typing import Optional
from uuid import UUID

from app.dependencies.database import database_dep
from app.entities import User


class UserRepository:
  def __init__(self, db: database_dep):
    self.db = db

  def create(
    self, team_id: UUID, competition_id: UUID, github_username: str, email: str
  ) -> User:
    user = User(
      team_id=team_id,
      competition_id=competition_id,
      github_username=github_username,
      email=email,
      username=None,
      password=None,
      registration_date=None,
    )
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)
    return user

  def save(self, user: User) -> User:
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)
    return user

  def get_by_id(self, user_id: UUID) -> Optional[User]:
    return self.db.query(User).filter(User.id == user_id).first()

  def get_by_email(self, email: str) -> Optional[User]:
    return self.db.query(User).filter(User.email == email).first()

  def delete(self, user: User):
    self.db.delete(user)
    self.db.commit()


def get_user_repository(db: database_dep) -> UserRepository:
  return UserRepository(db)
