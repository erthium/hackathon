"""
CommandRun Repository: This repository will be used to interact with the database for the CommandRun entity.
"""

from typing import Optional, List
from uuid import UUID

from app.dependencies.database import DatabaseDep
from app.entities import CommandRun
from app.objects.enums import RunCommandType


class CommandRunRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(
    self, release_id: UUID, run_command_type: RunCommandType, message: Optional[str] = None
  ) -> CommandRun:
    command_run = CommandRun(
      release_id=release_id,
      run_command_type=run_command_type,
      message=message
    )
    self.db.add(command_run)
    self.db.commit()
    self.db.refresh(command_run)
    return command_run

  def save(self, command_run: CommandRun) -> CommandRun:
    self.db.add(command_run)
    self.db.commit()
    self.db.refresh(command_run)
    return command_run

  def get_all(self) -> List[CommandRun]:
    return self.db.query(CommandRun).all()

  def get_by_id(self, template_id: UUID) -> Optional[CommandRun]:
    return self.db.query(CommandRun).filter(CommandRun.id == template_id).first()

  def delete(self, command_run: CommandRun):
    self.db.delete(command_run)
    self.db.commit()

  def delete_all(self):
    self.db.query(CommandRun).delete()
    self.db.commit()


def get_command_run_repository(db: DatabaseDep) -> CommandRunRepository:
  return CommandRunRepository(db)
