import os

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv(".env")
load_dotenv(dotenv_path)

GITHUB_PAT_TOKEN = os.getenv("GITHUB_PAT_TOKEN")
ENGINE_API_BASE_URL = os.getenv("ENGINE_API_BASE_URL")
assert GITHUB_PAT_TOKEN, "GITHUB_PAT_TOKEN is not set"
assert ENGINE_API_BASE_URL, "ENGINE_API_BASE_URL is not set"
