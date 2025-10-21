import os
import json
import stat
import time
import shutil
import asyncio
from typing import List
from pydantic import TypeAdapter, ValidationError

from app.core.settings import app_settings
from app.sandbox import build_and_run_sandbox
from app.objects.engine import CommandResult, CommandSuccessResult, CommandFailResult
from app.objects.template import Template, Command
from app.utils import TemplateUtils


async def run_sandbox(template: Template, command: Command, args: List[str]) -> CommandResult:

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
      cwd=clone_dir,
    )
    await git_clone_process.wait()
    if git_clone_process.returncode != 0:
      return CommandFailResult(error=f"Failed to clone the repo {repo_url}")

    repo_dir = os.path.join(clone_dir, repo_name)

    print("Checking out the commit...", flush=True)

    git_checkout_process = await asyncio.subprocess.create_subprocess_exec(
      "git",
      "checkout",
      commit_id,
      cwd=repo_dir,
    )

    await git_checkout_process.wait()
    if git_checkout_process.returncode != 0:
      return CommandFailResult(error=f"Failed to checkout the commit {commit_id} in the repo {arg}")

  print("Running the sandbox...", flush=True)

  # Prepare args
  prepared_args = [
    f"/sandbox/repo/{TemplateUtils.repo_to_args(arg)[1]}"  
    for arg in args
  ]



  # There is some timeout error handling logic going on,
  # but I commented out the part that throws that error in build_and_run_sandbox.
  # Still, no harm keeping these lines here.
  timeout_error = None
  try:
    docker_compose_up_process: asyncio.subprocess.Process = await build_and_run_sandbox(template.name, command.name, prepared_args)
  except TimeoutError:
    timeout_error = CommandFailResult(error="Time limit exceeded (10s)")
  except Exception as e:
    timeout_error = CommandFailResult(
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

  print("Cleaning up the sandbox directory...", flush=True)

  # Remove everything in the clone_dir, not the directory itself
  for item in os.listdir(clone_dir):
    item_path = os.path.join(clone_dir, item)
    if os.path.isdir(item_path):
      shutil.rmtree(item_path, onerror=on_rmtree_exc)
    else:
      os.remove(item_path)

  if timeout_error is not None:
    return timeout_error

  print("Sandbox run completed, checking the results...", flush=True)

  if docker_compose_up_process.returncode != 0:
    return CommandFailResult(error=stderr.decode())

  print("Sandbox run completed successfully, reading the results...", flush=True)

  # Check if the result file exists
  result_file_path = "sandbox/results/result.json"
  # list and print the tree of sandbox/results
  if os.path.exists("sandbox/results"):
    print("Sandbox results directory contents:", flush=True)
    for root, dirs, files in os.walk("sandbox/results"):
      print(f"Directory: {root}", flush=True)
      for file in files:
        print(f"  File: {file}", flush=True)
  else:
    print("Sandbox results directory does not exist.", flush=True)

  if not os.path.exists(result_file_path):
    return CommandFailResult(
      error="The result file does not exist. Make sure the command writes the result to 'sandbox/results/result.json'."
    )
  with open(result_file_path, "r") as results_file:
    all_content = results_file.read()
    print("All Result Content: ", all_content, flush=True)
    ta: TypeAdapter[CommandResult] = TypeAdapter(CommandResult)
    try:
      result = json.load(results_file)
      validated_result = ta.validate_python(result)
      return validated_result
    except ValidationError as e:
      return CommandFailResult(
        error=f"Error occurred validating the engine template's result: {e}"
      )
