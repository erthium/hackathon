import datetime
import typing
from typing import Optional

from app.objects.enums import ReleaseStatus
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .team import Team

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

  team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
  commit_id: Mapped[str] = mapped_column(unique=True, nullable=False)
  status: Mapped[ReleaseStatus] = mapped_column(
    default=ReleaseStatus.PENDING, init=False
  )
  message: Mapped[Optional[str]] = mapped_column(
    nullable=True, default=None, init=False
  )
  score: Mapped[Optional[float]] = mapped_column(
    nullable=True, default=None, init=False
  )
  release_date: Mapped[datetime.datetime] = (
    mapped_column()
  )  # Should be provided by GitHub's webhook

  team: Mapped["Team"] = relationship(back_populates="releases", init=False)

  def __repr__(self):
    return f"<Release {self.id} {self.commit_id}>"
