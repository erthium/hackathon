import os
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "../..", ".env")
assert os.path.exists(DOTENV_PATH), f"Settings file {DOTENV_PATH} does not exist"


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file=DOTENV_PATH, extra="ignore")

  BACKEND_BASE_URL: str = "http://localhost:8000"
  GITHUB_USERNAME: str = "owner_organisation"
  GITHUB_PAT_TOKEN: str = "token"
  TEMPLATES_DIR: str = "templates"
  DEVELOPMENT: bool = False


app_settings = Settings()
