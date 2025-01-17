import datetime
import typing
import uuid

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .competition_status import CompetitionStatus
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .team import Team

"""
Competition information:

Competition ID: UUID, Unique
Competition Name: Unique
Start Date (UTC)
End Date (UTC)
Status: Upcoming, Open, Ongoing, Completed
Winner Team ID: UUID, Nullable, Foreign Key
"""


class Competition(Base, IdMixin, AuditMixin):
  __tablename__ = "competitions"

  name: Mapped[str] = mapped_column(unique=True)
  start_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
  end_date: Mapped[datetime.datetime] = mapped_column()
  status: Mapped[CompetitionStatus] = mapped_column()
  winner_team_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("teams.id"), nullable=True
  )

  # Quotes provide forward referencing, preventing circular dependency: https://peps.python.org/pep-0484/#forward-references
  winner_team: Mapped["Team | None"] = relationship(back_populates="competition")
  teams: Mapped[list["Team"]] = relationship(back_populates="competition")

  def __repr__(self):
    return f"<Competition {self.id} {self.name}>"
