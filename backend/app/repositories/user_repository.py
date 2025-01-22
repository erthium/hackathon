"""
User Repository: This repository will be used to interact with the database for the User entity.
"""

from typing import Optional
from uuid import UUID

from app.entities import User
from dependencies.database import DatabaseDep


class UserRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(self, email: str, password: str) -> User:
    user = User(email=email, password=password)
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


def get_user_repository(db: DatabaseDep) -> UserRepository:
  return UserRepository(db)
