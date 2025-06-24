"""
Command Repository: This repository will be used to interact with the database for the Command entity.
"""

from typing import Optional
from uuid import UUID

from app.dependencies.database import DatabaseDep
from app.entities import Command
from app.objects.enums import CommandArgType


class CommandRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(
    self, template_id: UUID, name: str, arg_type: CommandArgType,
    allocated_ram: int, allocated_v_ram: int, allocated_cpu: int,
    description: Optional[str] = None, timeout: Optional[int] = None
  ) -> Command:
    command = Command(
      template_id=template_id,
      name=name,
      description=description,
      arg_type=arg_type,
      allocated_ram=allocated_ram,
      allocated_v_ram=allocated_v_ram,
      allocated_cpu=allocated_cpu,
      timeout=timeout,
    )
    self.db.add(command)
    self.db.commit()
    self.db.refresh(command)
    return command

  def save(self, command: Command) -> Command:
    self.db.add(command)
    self.db.commit()
    self.db.refresh(command)
    return command

  def get_by_id(self, command_id: UUID) -> Optional[Command]:
    return self.db.query(Command).filter(Command.id == command_id).first()

  def get_by_name_and_template_id(
    self, name: str, template_id: UUID
  ) -> Optional[Command]:
    return (
      self.db.query(Command)
      .filter(Command.name == name, Command.template_id == template_id)
      .first()
    )

  def delete(self, command: Command):
    self.db.delete(command)
    self.db.commit()

  def delete_all(self):
    self.db.query(Command).delete()
    self.db.commit()


def get_command_repository(db: DatabaseDep) -> CommandRepository:
  return CommandRepository(db)
