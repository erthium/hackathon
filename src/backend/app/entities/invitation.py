import datetime
import typing
import uuid

from app.objects.enums import InvitationEmailStatus, InvitationStatus
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .team import Team

"""
Invitation information:

Invitation Code: UUID, Unique
Team ID: UUID, Foreign Key
GitHub Username
Email
Invitation Email Status: Hasn't Sent, Sent, Had Error
Registration Date (UTC)
Expiration Date (UTC)
Status: Active, Expired, Used
"""


class Invitation(Base, IdMixin, AuditMixin):
  __tablename__ = "invitations"

  team_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("teams.id"))
  github_username: Mapped[str] = mapped_column()
  email: Mapped[str] = mapped_column()
  invitation_email_status: Mapped[InvitationEmailStatus] = mapped_column()
  registration_date: Mapped[datetime.datetime] = mapped_column(
    server_default=func.now()
  )
  expiration_date: Mapped[datetime.datetime] = mapped_column()
  status: Mapped[InvitationStatus] = mapped_column()

  team: Mapped["Team"] = relationship(back_populates="invitations")

  def __repr__(self):
    return f"<Invitation {self.id} {self.github_username}>"
