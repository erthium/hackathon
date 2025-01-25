import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


# https://gist.github.com/techniq/5174410
class AuditMixin(MappedAsDataclass):
  created_at: Mapped[datetime.datetime] = mapped_column(
    server_default=func.now(), init=False
  )
  updated_at: Mapped[datetime.datetime] = mapped_column(
    server_default=func.now(), onupdate=func.now(), init=False
  )
