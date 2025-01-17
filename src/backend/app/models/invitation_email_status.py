import enum


class InvitationEmailStatus(enum.Enum):
  NOT_SENT = "hasn't sent"
  SENT = "sent"
  HAD_ERROR = "had error"
