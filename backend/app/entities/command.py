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
Command information:

Command ID: UUID, Unique
Command Name: Unique
Command Description: Optional
Command Argument Type: Enum (e.g., STRING, INTEGER, BOOLEAN)
Command Allocated RAM: Integer (in MB)
Command Allocated Virtual RAM: Integer (in MB)
Command Allocated CPU: Integer (in percentage)
Command Timeout: Optional Integer (in seconds)
Command Template ID: Foreign Key to Template
"""


class Command(Base, IdMixin, AuditMixin):
  __tablename__ = "commands"

  # Columns
  template_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("templates.id"), nullable=False)
  name: Mapped[str] = mapped_column(nullable=False)
  description: Mapped[str] = mapped_column(nullable=True)
  arg_type: Mapped[CommandArgType] = mapped_column(nullable=False)
  allocated_ram: Mapped[int] = mapped_column(nullable=False)
  allocated_v_ram: Mapped[int] = mapped_column(nullable=False)
  allocated_cpu: Mapped[int] = mapped_column(nullable=False)
  timeout: Mapped[Optional[int]] = mapped_column(nullable=True)

  # Relationships
  template: Mapped["Template"] = relationship(back_populates="commands", init=False)


  def __repr__(self):
    return f"<Command {self.id} {self.name}>"
