import uuid

from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class IdMixin(MappedAsDataclass):
  id: Mapped[uuid.UUID] = mapped_column(
    primary_key=True,
    default_factory=uuid.uuid4,
    init=False,
    sort_order=-1,  # Defaults to 0, so setting to -1 makes it the first column
  )
