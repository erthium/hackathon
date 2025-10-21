import datetime
import typing
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

from app.objects.enums import RunCommandType

if typing.TYPE_CHECKING:
  from .release import Release
  from .score import Score


"""
Command Run information:

release_id: UUID, Foreign Key to Release
run_command_type: RunCommandType, the type of command run
message: Optional[str], a message associated with the command run
"""


class CommandRun(Base, IdMixin, AuditMixin):
  __tablename__ = "command_runs"

  # Columns
  release_id: Mapped[UUID] = mapped_column(
    ForeignKey("releases.id"), nullable=False
  )
  run_command_type: Mapped[RunCommandType] = mapped_column(
    nullable=False, init=False
  )
  message: Mapped[Optional[str]] = mapped_column(
    nullable=True, default=None, init=False
  )

  # Relationships
  release: Mapped["Release"] = relationship(
    back_populates="command_runs", init=False
  )
  scores: Mapped[list["Score"]] = relationship(
    back_populates="command_runs", default_factory=list, init=False
  )


  def __repr__(self):
    return f"<Release {self.id} {self.commit_id}>"
