import asyncio
import json
import os
import shutil
import stat
import time
from pydantic import TypeAdapter, ValidationError
from typing import List
import asyncio

from app.objects.engine import EngineTestFailedResult, EngineTestResult
from app.sandbox import build_and_run_sandbox
from app.core.settings import app_settings
from app.objects.template import Template, Command
from app.utils import TemplateUtils


async def run_sandbox(template: Template, command: Command, args: List[str]) -> EngineTestResult:

  clone_dir = "/engine/sandbox/repo"
  github_username = app_settings.GITHUB_USERNAME
  github_pat_token = app_settings.GITHUB_PAT_TOKEN
  for arg in args:
    assert TemplateUtils.is_repo_str_valid(arg), f"Invalid repo string: {arg}"
    repo_owner, repo_name, commit_id = TemplateUtils.repo_to_args(arg)
    repo_url = f"https://{github_username}:{github_pat_token}@github.com/{repo_owner}/{repo_name}.git"

    print(f"Cloning the repo {arg}", flush=True)

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
    if git_checkout_process.returncode != 0:
      return EngineTestFailedResult(error=f"Failed to checkout the commit {commit_id} in the repo {arg}")


  # There is some timeout error handling logic going on,
  # but I commented out the part that throws that error in build_and_run_sandbox.
  # Still, no harm keeping these lines here.
  timeout_error = None
  try:
    docker_compose_up_process: asyncio.subprocess.Process = await build_and_run_sandbox(template.name, command.name, args)
  except TimeoutError:
    timeout_error = EngineTestFailedResult(error="Time limit exceeded (10s)")
  except Exception as e:
    timeout_error = EngineTestFailedResult(
      error=f"An error occurred running the sandbox: {e}"
    )

  if timeout_error is None:
    stdout, stderr = await docker_compose_up_process.communicate()

    print(stdout.decode(), flush=True)
    print(stderr.decode(), flush=True)

    await docker_compose_up_process.wait()

  # Some Windows problems if I remember correctly (when will this code run on Windows exactly xD)
  def on_rmtree_exc(func, path, exc_info):
    os.chmod(path, stat.S_IWUSR)
    func(path)

  # This is for waiting the above command to finish
  # Without this, shutil.rmtree below doesn't work properly
  time.sleep(1)

  shutil.rmtree(clone_dir, onexc=on_rmtree_exc)

  if timeout_error is not None:
    return timeout_error

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
