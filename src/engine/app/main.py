from fastapi import FastAPI

from .commands.test import test

app = FastAPI()


@app.get("/{repo_owner}/{repo_name}/releases/{release_tag}")
async def run_engine(repo_owner: str, repo_name: str, release_tag: str):
    # Temporary implementation, will support evaluation also
    return test(repo_owner, repo_name, release_tag)
