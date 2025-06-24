import typing
import uuid
from typing import Optional

from app.entities.base import Base
from app.entities.mixins import AuditMixin, IdMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.objects.enums import RunCommandType

if typing.TYPE_CHECKING:
  from .score_metric import ScoreMetric
  from .release import Release

"""
Score information:

score_metric_id: UUID
release_id: UUID
value: float, the score value
run_command_type: RunCommandType, the type of command used to calculate the score
"""


class Score(Base, IdMixin, AuditMixin):
  __tablename__ = "scores"

  # Columns
  score_metric_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("score_metrics.id"), nullable=False
  )
  release_id: Mapped[Optional[uuid.UUID]] = mapped_column(
    ForeignKey("releases.id"), nullable=True
  )
  value: Mapped[float] = mapped_column(nullable=False)
  run_command_type: Mapped[RunCommandType] = mapped_column(
    nullable=False, init=False
  )

  # Relationships
  score_metric: Mapped["ScoreMetric"] = relationship(
    back_populates="scores", init=False
  )
  release: Mapped[Optional["Release"]] = relationship(
    back_populates="scores", init=False
  )

  def __repr__(self):
    return f"<Score {self.id} {self.value}>"
