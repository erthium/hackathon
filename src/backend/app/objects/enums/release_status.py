import enum


class ReleaseStatus(enum.Enum):
  PENDING = "pending"
  APPROVED = "approved"
  REJECTED = "rejected"
