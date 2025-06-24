import typing
import uuid
from typing import Optional, List

from app.entities.base import Base
from app.entities.mixins import AuditMixin, IdMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
  from .template import Template
  from .score import Score

"""
Score Metric information:

Score Metric ID: UUID, Unique
Template ID: UUID, Foreign Key to Template
Name: Unique
Description: Optional
Is Ascending: bool, whether higher values are better
Is Primary: bool, whether this is the primary score metric for the template
Is Public: bool, whether this score metric is public
Min Value: Optional[float], minimum value for the score metric
Max Value: Optional[float], maximum value for the score metric
"""


class ScoreMetric(Base, IdMixin, AuditMixin):
  __tablename__ = "score_metrics"

  # Columns
  template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("templates.id"), nullable=False)
  name: Mapped[str] = mapped_column(nullable=False)
  description: Mapped[str] = mapped_column(nullable=True)
  is_ascending: Mapped[bool] = mapped_column(nullable=False, default=True)
  is_primary: Mapped[bool] = mapped_column(nullable=False, default=False)
  is_public: Mapped[bool] = mapped_column(nullable=False, default=True)
  min_value: Mapped[Optional[float]] = mapped_column(nullable=True, default=None)
  max_value: Mapped[Optional[float]] = mapped_column(nullable=True, default=None)

  # Relationships
  template: Mapped["Template"] = relationship(back_populates="score_metrics", init=False)
  scores: Mapped[List["Score"]] = relationship(back_populates="score_metric", init=False)


  def __repr__(self):
    return f"<Score Metric {self.id} {self.name}>"
