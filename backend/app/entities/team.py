import datetime
import typing
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import team_user_association
from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .competition import Competition
  from .release import Release
  from .user import User

"""
Team information:

Team ID: UUID, Unique
Competition ID: UUID, Foreign Key
Team Name: Predecided before invitation, unique for each competition
GitHub Repository: Unique
Registration Date (UTC)
"""


class Team(Base, IdMixin, AuditMixin):
  __tablename__ = "teams"

  competition_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey(
      "competitions.id",
      use_alter=True,  # Since it forms a circular dependency
    )
  )
  name: Mapped[str] = mapped_column(nullable=False)
  github_repo: Mapped[str] = mapped_column(unique=True, nullable=False)
  registration_date: Mapped[datetime.datetime] = mapped_column(
    server_default=func.now()
  )

  competition: Mapped["Competition"] = relationship(back_populates="teams")
  members: Mapped[list["User"]] = relationship(
    secondary=team_user_association, back_populates="teams"
  )
  releases: Mapped[list["Release"]] = relationship(back_populates="team")

  __table_args__ = (
    # Team name should be unique for each competition
    UniqueConstraint("competition_id", "name"),
  )

  def __repr__(self):
    return f"<Team {self.id} {self.name}>"
