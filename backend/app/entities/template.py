import typing

from app.entities.base import Base
from app.entities.mixins import AuditMixin, IdMixin
from app.entities.command import Command
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
  from .command import Command

"""
Template information:

Template ID: UUID, Unique
Template Name: Unique
Template Description: Optional
Template Author: Optional
"""


class Template(Base, IdMixin, AuditMixin):
  __tablename__ = "templates"

  name: Mapped[str] = mapped_column(unique=True, nullable=False)
  description: Mapped[str] = mapped_column(nullable=True)
  author: Mapped[str] = mapped_column(nullable=True)

  commands: Mapped[list["Command"]] = relationship(
    back_populates="template", default_factory=list, init=False
  )


  def __repr__(self):
    return f"<Template {self.id} {self.name}>"
