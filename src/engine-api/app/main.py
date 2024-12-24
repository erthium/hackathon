import subprocess

from fastapi import FastAPI

app = FastAPI()


@app.get("/{repo_owner}/{repo_name}/releases/{release_tag}")
async def run_engine(repo_owner: str, repo_name: str, release_tag: str):
    p = subprocess.run(
        ["py", "../../engine/main.py", "test", repo_owner, repo_name, release_tag],
        capture_output=True,
    )
    return {"message": p.stdout.decode()}
