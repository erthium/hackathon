from sqlalchemy import create_engine

from .settings import app_settings

engine = create_engine(app_settings.db_url, echo=True)
