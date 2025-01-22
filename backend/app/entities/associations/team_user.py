from sqlalchemy import Column, ForeignKey, Table

from ..base import Base

team_user_association = Table(
  "team_user",
  Base.metadata,
  Column("team_id", ForeignKey("teams.id"), primary_key=True),
  Column("user_id", ForeignKey("users.id"), primary_key=True),
)
