import os
import shutil
import stat
import subprocess
import time

from ..sandbox import build_and_run_sandbox


# The current implementation is for testing purposes only
def test(repo_owner: str, repo_name: str, release_tag: str):
  docker_compose_up_process = build_and_run_sandbox()

  if docker_compose_up_process.returncode != 0:
    return docker_compose_up_process.stderr.decode()

  return docker_compose_up_process.stdout.decode()

  repo_url = f"https://github.com/{repo_owner}/{repo_name}.git"

  os.mkdir(f"{repo_name}")

  subprocess.run(
    [
      "git",
      "clone",
      repo_url,
      "-b",
      release_tag,
    ]
  )

  # Some Windows problems if I remember correctly
  def on_rmtree_exc(func, path, exc_info):
    os.chmod(path, stat.S_IWUSR)
    func(path)

  # This is for waiting the above command to finish
  # Without this, shutil.rmtree below doesn't work properly
  time.sleep(1)

  shutil.rmtree(repo_name, onexc=on_rmtree_exc)

  return {"message": f"Successfully cloned and deleted the repo {repo_url}"}
