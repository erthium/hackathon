import datetime
import typing
from typing import Optional
from uuid import UUID

from app.objects.enums import ReleaseStatus
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .team import Team
  from .command_run import CommandRun

"""
Release information:

Release ID: UUID, Unique
Team ID: UUID, Foreign Key
Commit ID: Unique
Status: Pending (default), Approved, Rejected
Message: Optional
Score: Optional
Release Date (UTC)
"""


class Release(Base, IdMixin, AuditMixin):
  __tablename__ = "releases"

  # Columns
  team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"))
  commit_id: Mapped[str] = mapped_column(unique=True, nullable=False)
  status: Mapped[ReleaseStatus] = mapped_column(
    default=ReleaseStatus.PENDING, init=False
  )
  # Should be provided by GitHub's webhook
  release_date: Mapped[datetime.datetime] = (
    mapped_column()
  )

  # Relationships
  team: Mapped["Team"] = relationship(
    back_populates="releases", init=False
  )
  command_runs: Mapped[list["CommandRun"]] = relationship(
    back_populates="release", default_factory=list, init=False
  )


  def __repr__(self):
    return f"<Release {self.id} {self.commit_id}>"
