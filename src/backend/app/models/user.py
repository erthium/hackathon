import datetime
import typing
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .team import Team

"""
User information:

User ID: UUID, Unique
Team ID: UUID, Foreign Key
GitHub Username: Unique
Email: Unique for each competition
Username: Unique for each competition
Name
Registration Date (UTC)
"""


class User(Base, IdMixin, AuditMixin):
  __tablename__ = "users"

  team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"))
  github_username: Mapped[str] = mapped_column()
  email: Mapped[str] = mapped_column()
  username: Mapped[str] = mapped_column()
  name: Mapped[str] = mapped_column()
  registration_date: Mapped[datetime.datetime] = mapped_column(
    server_default=func.now()
  )

  team: Mapped["Team"] = relationship(back_populates="members")

  __table_args__ = (
    # GitHub username should be unique for each team
    UniqueConstraint("team_id", "github_username"),
    # Email should be unique for each team
    UniqueConstraint("team_id", "email"),
    # Username should be unique for each team
    UniqueConstraint("team_id", "username"),
  )

  def __repr__(self):
    return f"<User {self.id} {self.github_username}>"
