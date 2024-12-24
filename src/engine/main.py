import os
import shutil
import stat
import subprocess
import time

import typer

app = typer.Typer()


@app.command()
def test(repo_owner: str, repo_name: str, release_tag: str):
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

    def on_rmtree_exc(func, path, exc_info):
        os.chmod(path, stat.S_IWUSR)
        func(path)

    time.sleep(1)

    shutil.rmtree(repo_name, onexc=on_rmtree_exc)

    print(f"Successfully cloned and deleted the repo {repo_url}")


# for enabling single command
@app.callback()
def callback():
    pass


if __name__ == "__main__":
    app()
