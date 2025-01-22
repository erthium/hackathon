import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=DOTENV_PATH, extra="ignore")

  BACKEND_BASE_URL: str = ""
  GITHUB_USERNAME: str = ""
  GITHUB_PAT_TOKEN: str = ""


app_settings = Settings()
