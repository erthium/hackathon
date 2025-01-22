from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.settings import app_settings

engine = create_engine(app_settings.DB_URL, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(SessionFactory)

def get_database():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
