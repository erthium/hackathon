"""
Release Repository: This repository will be used to interact with the database for the Release entity.
"""

from typing import Optional
from uuid import UUID

from app.entities import Release
from dependencies.database import DatabaseDep


class ReleaseRepository:
  def __init__(self, db: DatabaseDep):
    self.db = db

  def create(self, version: str, release_date: str, description: str) -> Release:
    release = Release(
      version=version,
      release_date=release_date,
      description=description,
    )
    self.db.add(release)
    self.db.commit()
    self.db.refresh(release)
    return release

  def save(self, release: Release) -> Release:
    self.db.add(release)
    self.db.commit()
    self.db.refresh(release)
    return release

  def get_by_id(self, release_id: UUID) -> Optional[Release]:
    return self.db.query(Release).filter(Release.id == release_id).first()

  def delete(self, release: Release):
    self.db.delete(release)
    self.db.commit()


def get_release_repository(db: DatabaseDep) -> ReleaseRepository:
  return ReleaseRepository(db)
