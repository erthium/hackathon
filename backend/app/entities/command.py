import typing
import uuid
from typing import Optional

from app.entities.base import Base
from app.entities.mixins import AuditMixin, IdMixin
from app.objects.enums import CommandArgType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if typing.TYPE_CHECKING:
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


class Command(Base, IdMixin, AuditMixin):
  __tablename__ = "commands"

  template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("templates.id"), nullable=False)
  name: Mapped[str] = mapped_column(nullable=False)
  description: Mapped[str] = mapped_column(nullable=True)
  arg_type: Mapped[CommandArgType] = mapped_column(nullable=False)
  allocated_ram: Mapped[int] = mapped_column(nullable=False)
  allocated_v_ram: Mapped[int] = mapped_column(nullable=False)
  allocated_cpu: Mapped[int] = mapped_column(nullable=False)
  timeout: Mapped[Optional[int]] = mapped_column(nullable=True)

  template: Mapped["Template"] = relationship(back_populates="commands", init=False)


  def __repr__(self):
    return f"<Command {self.id} {self.name}>"
