"""
Release Repository: This repository will be used to interact with the database for the Release entity.
"""

import datetime
from typing import List, Optional
from uuid import UUID

from app.dependencies.database import database_dep
from app.entities import Release


class ReleaseRepository:
  def __init__(self, db: database_dep):
    self.db = db

  def create(
    self, team_id: UUID, commit_id: str, release_date: datetime.datetime
  ) -> Release:
    release = Release(
      commit_id=commit_id,
      team_id=team_id,
      release_date=release_date,
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

  def get_latest_by_team_id(self, team_id) -> Optional[Release]:
    return (
      self.db.query(Release)
      .filter(Release.team_id == team_id)
      .order_by(Release.release_date.desc())
      .first()
    )

  def get_all_by_team_id(self, team_id) -> List[Release]:
    return self.db.query(Release).filter(Release.team_id == team_id).all()

  def get_all(self) -> List[Release]:
    return self.db.query(Release).all()


def get_release_repository(db: database_dep) -> ReleaseRepository:
  return ReleaseRepository(db)
