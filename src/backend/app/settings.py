import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)

    github_pat_token: str = "token"
    engine_api_base_url: str = "http://localhost:8001"
    db_url: str = "postgresql://user:password@localhost:5432/db"
    redis_url: str = "redis://localhost"
    redis_password: str = "password"


app_settings = Settings()
