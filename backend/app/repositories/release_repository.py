"""
Release Repository: This repository will be used to interact with the database for the Release entity.
"""

import datetime
from uuid import UUID
from sqlalchemy import select
from typing import List, Optional, Sequence

from app.dependencies.database import DatabaseDep
from app.entities import Release
from app.utils import TimeUtils


class ReleaseRepository:
  def __init__(self, db: DatabaseDep):
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

  def get_release_count_today(self, team_id: UUID) -> int:
    today = TimeUtils.get_datetime_today()
    return (
      self.db.query(Release)
      .filter(
        Release.team_id == team_id,
        Release.release_date >= today,
        Release.release_date < today + datetime.timedelta(days=1),
      )
      .count()
    )

  def get_total_release_count(self, team_id: UUID) -> int:
    return (
      self.db.query(Release)
      .filter(Release.team_id == team_id)
      .count()
    )

  def get_all(self) -> Sequence[Release]:
    # The SQLAlchemy 2.0 way:
    # https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
    return self.db.scalars(select(Release)).all()


def get_release_repository(db: DatabaseDep) -> ReleaseRepository:
  return ReleaseRepository(db)
