import typing

from app.entities.base import Base
from app.entities.mixins import AuditMixin, IdMixin
from app.entities.command import Command
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
  from .score_metric import ScoreMetric
  from .command import Command
  from .competition import Competition

"""
Template information:

Template ID: UUID, Unique
Template Name: Unique
Template Description: Optional
Template Author: Optional

"""


class Template(Base, IdMixin, AuditMixin):
  __tablename__ = "templates"

  # Columns
  name: Mapped[str] = mapped_column(unique=True, nullable=False)
  description: Mapped[str] = mapped_column(nullable=True)
  author: Mapped[str] = mapped_column(nullable=True)

  on_submission_command: Mapped[str] = mapped_column(
    nullable=True, default=None
  )
  on_competition_end_command: Mapped[str] = mapped_column(
    nullable=True, default=None
  )

  # Relationships
  score_metrics: Mapped[list["ScoreMetric"]] = relationship(
    back_populates="template", default_factory=list, init=False
  )
  commands: Mapped[list["Command"]] = relationship(
    back_populates="template", default_factory=list, init=False
  )
  competitions: Mapped[list["Competition"]] = relationship(
    back_populates="template", default_factory=list, init=False
  )


  def __repr__(self):
    return f"<Template {self.id} {self.name}>"
