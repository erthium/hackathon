import datetime
import typing
import uuid
from typing import Optional

from app.entities.base import Base
from app.entities.mixins import AuditMixin, IdMixin
from app.objects.enums import CompetitionStatus
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
  from .team import Team
  from .template import Template

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

  # Columns
  name: Mapped[str] = mapped_column(unique=True, nullable=False)
  start_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)
  end_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)
  status: Mapped[CompetitionStatus] = mapped_column(
    default=CompetitionStatus.UPCOMING, init=False
  )
  winner_team_id: Mapped[Optional[uuid.UUID]] = mapped_column(
    ForeignKey("teams.id"), nullable=True, init=False
  )
  # Template name is optional, as competitions can be created without a template and it can be added/changed later
  template_name: Mapped[Optional[str]] = mapped_column(
    ForeignKey("templates.name"), nullable=True, init=False
  )

  # Relationships
  # Quotes provide forward referencing, preventing circular dependency: https://peps.python.org/pep-0484/#forward-references
  winner_team: Mapped["Team | None"] = relationship(
    back_populates="competition",
    foreign_keys=[winner_team_id],
    init=False,
  )
  teams: Mapped[list["Team"]] = relationship(
    back_populates="competition",
    foreign_keys="Team.competition_id",
    default_factory=list,
  )
  template: Mapped[Optional["Template"]] = relationship(
    back_populates="competitions",
    foreign_keys=[template_name],
    init=False,
  )


  def __repr__(self):
    return f"<Competition {self.id} {self.name}>"
