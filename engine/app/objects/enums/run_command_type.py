from enum import Enum


class RunCommandType(Enum):
  ON_SUBMISSION = "on_submission"
  ON_COMPETITION_END = "on_competition_end"
  OTHER = "other"  
