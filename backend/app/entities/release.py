import datetime
import typing

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
Commit ID
Status: Pending, Approved, Rejected
Message: Reason for rejection
Release Date (UTC)
"""


class Release(Base, IdMixin, AuditMixin):
  __tablename__ = "releases"

  commit_id: Mapped[str] = mapped_column(unique=True)
  team_id: Mapped[str] = mapped_column(ForeignKey("teams.id"))
  status: Mapped[ReleaseStatus] = mapped_column()
  message: Mapped[str] = mapped_column()
  release_date: Mapped[datetime.datetime] = (
    mapped_column()
  )  # Should be provided by GitHub's webhook

  team: Mapped["Team"] = relationship(back_populates="releases")

  def __repr__(self):
    return f"<Release {self.id} {self.commit_id}>"
