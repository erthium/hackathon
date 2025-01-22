import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


# https://gist.github.com/techniq/5174410
class AuditMixin:
  created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
  updated_at: Mapped[datetime.datetime] = mapped_column(
    server_default=func.now(), onupdate=func.now()
  )
