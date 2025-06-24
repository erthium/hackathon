"""
Template Repository: This repository will be used to interact with the database for the Template entity.
"""

from typing import Optional, List
from uuid import UUID

from app.dependencies.database import DatabaseDep
from app.entities import Template


class TemplateRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(
    self, name: str, description: Optional[str] = None, author: Optional[str] = None
  ) -> Template:
    template = Template(
      name=name,
      description=description,
      author=author,
    )
    self.db.add(template)
    self.db.commit()
    self.db.refresh(template)
    return template

  def save(self, template: Template) -> Template:
    self.db.add(template)
    self.db.commit()
    self.db.refresh(template)
    return template

  def get_all(self) -> List[Template]:
    return self.db.query(Template).all()

  def get_by_id(self, template_id: UUID) -> Optional[Template]:
    return self.db.query(Template).filter(Template.id == template_id).first()

  def get_by_name(self, name: str) -> Optional[Template]:
    return self.db.query(Template).filter(Template.name == name).first()

  def delete(self, template: Template):
    self.db.delete(template)
    self.db.commit()

  def delete_all(self):
    self.db.query(Template).delete()
    self.db.commit()


def get_template_repository(db: DatabaseDep) -> TemplateRepository:
  return TemplateRepository(db)
