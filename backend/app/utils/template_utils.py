from typing import List


class TemplateUtils:
  @staticmethod
  def is_repo_str_valid(repo: str) -> bool:
    """
    This method is used to validate the repo string
    """
    repo_args = repo.split("/")
    if len(repo_args) != 3:
      return False

    if not all(repo_args):
      return False

    return True

  @staticmethod
  def repo_args_to_str(repo_owner: str, repo_name: str, commit_id: str) -> str:
    """
    This method is used to convert the repo arguments to a string
    """
    return f"{repo_owner}/{repo_name}/{commit_id}"


  @staticmethod
  def repo_to_args(repo: str) -> List[str]:
    """
    This method is used to convert the repo string to arguments
    """
    return repo.split("/")
