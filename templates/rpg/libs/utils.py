"""
This script curates the functions that are used in both test.py and evaluate.py
"""

import os
from dynamic_import import import_attribute
from base_agent import BaseAgent

# Constants
MODULE_DIR = "src"
MODULE_NAME = "agent"
ATTRIBUTE_NAME = "Agent"
REQUIRED_FILES_IN_ROOT = ["requirements.txt"]

def generate_seed() -> str:
  """
  Generate a seed for the fight
  """
  return os.urandom(16).hex()


def directory_checks(agent_repo: str):
  """
  Check if the cloned repository has the required structure
  """
  assert os.path.exists(agent_repo) and os.path.isdir(agent_repo), f"Agent repo {agent_repo} is not a valid directory"
  assert os.path.exists(os.path.join(agent_repo, MODULE_DIR)), f"Agent repo {agent_repo} does not contain a '{MODULE_DIR}' directory"
  assert os.path.exists(os.path.join(agent_repo, MODULE_DIR, f"{MODULE_NAME}.py")), f"Agent repo {agent_repo} does not contain a '{MODULE_NAME}.py' file in the '{MODULE_DIR}' directory"
  for required_file in REQUIRED_FILES_IN_ROOT:
    assert os.path.exists(os.path.join(agent_repo, required_file)), f"Agent repo {agent_repo} does not contain a '{required_file}' file in the root directory"


def get_agent_from_repo(agent_repo: str, seed: str) -> BaseAgent:
  path_to_agent = os.path.join(agent_repo, MODULE_DIR)
  Agent: BaseAgent = import_attribute(path_to_agent, MODULE_NAME, ATTRIBUTE_NAME)
  return Agent(name="SupposedlyContestantAgent", seed=seed)
