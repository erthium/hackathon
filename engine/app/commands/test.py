import asyncio
import json
import os
import shutil
import stat
import time

from app.objects.engine import EngineTestFailedResult, EngineTestResult
from app.sandbox import build_and_run_sandbox
from app.settings import app_settings
from pydantic import TypeAdapter, ValidationError


# The current implementation is for testing purposes only
async def test(repo_owner: str, repo_name: str, commit_id: str) -> EngineTestResult:
  github_username = app_settings.GITHUB_USERNAME
  github_pat_token = app_settings.GITHUB_PAT_TOKEN
  repo_url = f"https://{github_username}:{github_pat_token}@github.com/{repo_owner}/{repo_name}.git"
  clone_dir = "/engine/sandbox/repo"

  print("Cloning the repo...", flush=True)

  git_clone_process = await asyncio.subprocess.create_subprocess_exec(
    "git",
    "clone",
    repo_url,
    clone_dir,
  )

  await git_clone_process.wait()

  if git_clone_process.returncode != 0:
    return EngineTestFailedResult(error=f"Failed to clone the repo {repo_url}")

  print("Checking out the commit...", flush=True)

  git_checkout_process = await asyncio.subprocess.create_subprocess_exec(
    "git",
    "checkout",
    commit_id,
    cwd=clone_dir,
  )

  await git_checkout_process.wait()

  docker_compose_up_process = await build_and_run_sandbox()

  stdout, stderr = await docker_compose_up_process.communicate()

  print(stdout.decode(), flush=True)
  print(stderr.decode(), flush=True)

  await docker_compose_up_process.wait()

  # Some Windows problems if I remember correctly
  def on_rmtree_exc(func, path, exc_info):
    os.chmod(path, stat.S_IWUSR)
    func(path)

  # This is for waiting the above command to finish
  # Without this, shutil.rmtree below doesn't work properly
  time.sleep(1)

  shutil.rmtree(clone_dir, onexc=on_rmtree_exc)

  if docker_compose_up_process.returncode != 0:
    return EngineTestFailedResult(error=stderr.decode())

  with open("sandbox/results/result.json", "r") as results_file:
    ta: TypeAdapter[EngineTestResult] = TypeAdapter(EngineTestResult)
    try:
      result = json.load(results_file)
      validated_result = ta.validate_python(result)
      return validated_result
    except ValidationError as e:
      return EngineTestFailedResult(
        error=f"Error occurred validating the engine template's result: {e}"
      )

  # return EngineTestSucceededResult(
  #   result=f"Successfully cloned and deleted the repo {repo_url}"
  # )
