import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "../..", ".env")


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=DOTENV_PATH, extra="ignore")

  GITHUB_PAT_TOKEN: str = "token"
  ENGINE_API_BASE_URL: str = "http://localhost:8001"
  DB_URL: str = "postgresql://user:password@localhost:5432/db"
  REDIS_URL: str = "redis://localhost"
  REDIS_PASSWORD: str = "password"

  DEVELOPMENT: bool = False


app_settings = Settings()
