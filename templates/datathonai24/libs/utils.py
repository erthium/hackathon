"""
This script curates the functions that are used in the template
"""

import os

from dynamic_import import import_attribute

# Repository Constants
MODULE_DIR = "src"
MODULE_NAME = "main"
ATTRIBUTE_NAME = "predict"
REQUIRED_FILES_IN_ROOT = ["requirements.txt"]


def directory_checks(repository_path: str):
  """
  Check if the cloned repository has the required structure
  """
  assert os.path.exists(repository_path) and os.path.isdir(repository_path), f"Repo {repository_path} is not a valid directory"
  assert os.path.exists(os.path.join(repository_path, MODULE_DIR)), f"Repo {repository_path} does not contain a '{MODULE_DIR}' directory"
  assert os.path.exists(os.path.join(repository_path, MODULE_DIR, f"{MODULE_NAME}.py")), f"Repo {repository_path} does not contain a '{MODULE_NAME}.py' file in the '{MODULE_DIR}' directory"
  for required_file in REQUIRED_FILES_IN_ROOT:
    assert os.path.exists(os.path.join(repository_path, required_file)), f"Repo {repository_path} does not contain a '{required_file}' file in the root directory"


def get_predict_from_repo(repository_path: str) -> callable:
  path_to_main = os.path.join(repository_path, MODULE_DIR)
  predict: callable = import_attribute(path_to_main, MODULE_NAME, ATTRIBUTE_NAME)
  return predict


