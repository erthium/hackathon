import uuid

from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
  id: Mapped[uuid.UUID] = mapped_column(
    primary_key=True,
    default=uuid.uuid4,
    sort_order=-1,  # Defaults to 0, so setting to -1 makes it the first column
  )
