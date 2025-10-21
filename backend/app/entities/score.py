import typing
import uuid
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .score_metric import ScoreMetric
  from .command_run import CommandRun

"""
Score information:

score_metric_id: UUID
command_run_id: UUID
value: float, the score value
"""


class Score(Base, IdMixin, AuditMixin):
  __tablename__ = "scores"

  # Columns
  score_metric_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("score_metrics.id"), nullable=False
  )
  command_run_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("command_runs.id"), nullable=False
  )
  value: Mapped[float] = mapped_column(nullable=False)

  # Relationships
  score_metric: Mapped["ScoreMetric"] = relationship(
    back_populates="scores", init=False
  )
  command_run: Mapped[Optional["CommandRun"]] = relationship(
    back_populates="scores", init=False
  )

  def __repr__(self):
    return f"<Score {self.id} {self.value}>"
