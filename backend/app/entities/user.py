import datetime
import typing
import uuid
from typing import Optional

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .invitation import Invitation
  from .team import Team

"""
User information:

User ID: UUID, Unique
Team ID: UUID, Foreign Key
GitHub Username: Unique
Email: Unique for each competition
Username: Unique for each competition, Optional
Registration Date (UTC): Optional
"""


class User(Base, IdMixin, AuditMixin):
  __tablename__ = "users"

  team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)
  competition_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("competitions.id"), nullable=False
  )
  github_username: Mapped[str] = mapped_column(nullable=False)
  email: Mapped[str] = mapped_column(nullable=False)
  username: Mapped[Optional[str]] = mapped_column(nullable=True)
  password: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
  registration_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

  invitation: Mapped["Invitation"] = relationship(back_populates="user")
  team: Mapped["Team"] = relationship(back_populates="members")

  __table_args__ = (
    # GitHub username should be unique for each competition
    UniqueConstraint("competition_id", "github_username"),
    # Email should be unique for each competition
    UniqueConstraint("competition_id", "email"),
    # Username should be unique for each competition
    UniqueConstraint("competition_id", "username"),
  )

  def __repr__(self):
    return f"<User {self.id} {self.github_username}>"
