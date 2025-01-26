import datetime
import typing
import uuid

from app.objects.enums import InvitationEmailStatus, InvitationStatus
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import AuditMixin, IdMixin

if typing.TYPE_CHECKING:
  from .user import User

"""
Invitation information:

Invitation Code: UUID, Unique
User ID: UUID, Foreign Key
Status: Active (default), Used, Expired
Invitation Email Status: Not Sent (default), Sent, Had Error
Expiration Date (UTC): Optional
"""


class Invitation(Base, IdMixin, AuditMixin):
  __tablename__ = "invitations"

  user_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("users.id"), unique=True, nullable=False
  )
  invitation_code: Mapped[str] = mapped_column(unique=True, nullable=False)
  status: Mapped[InvitationStatus] = mapped_column(default=InvitationStatus.ACTIVE)
  invitation_email_status: Mapped[InvitationEmailStatus] = mapped_column(
    default=InvitationEmailStatus.NOT_SENT
  )
  expiration_date: Mapped[datetime.datetime] = mapped_column(
    nullable=True, default=None
  )

  user: Mapped["User"] = relationship(back_populates="invitation", init=False)

  def __repr__(self):
    return f"<Invitation {self.id} {self.user_id}>"
