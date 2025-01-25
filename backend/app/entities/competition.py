import datetime
import typing
import uuid
from typing import Optional

from app.objects.enums import CompetitionStatus
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .team import Team

"""
Competition information:

Competition ID: UUID, Unique
Competition Name: Unique
Start Date (UTC): Optional
End Date (UTC): Optional
Status: Upcoming (default), Ongoing, Ended
Winner Team ID: Optional
"""


class Competition(Base, IdMixin, AuditMixin):
  __tablename__ = "competitions"

  name: Mapped[str] = mapped_column(unique=True, nullable=False)
  start_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)
  end_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)
  status: Mapped[CompetitionStatus] = mapped_column(default=CompetitionStatus.UPCOMING)
  winner_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(
    ForeignKey("teams.id"), nullable=True
  )

  # Quotes provide forward referencing, preventing circular dependency: https://peps.python.org/pep-0484/#forward-references
  winner_team: Mapped["Team | None"] = relationship(back_populates="competition")
  teams: Mapped[list["Team"]] = relationship(back_populates="competition")

  def __repr__(self):
    return f"<Competition {self.id} {self.name}>"
