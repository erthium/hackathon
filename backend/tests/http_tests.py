import os
import requests
from dotenv import load_dotenv
from random import randint
from time import sleep
import subprocess
import json

# Load environment variables from .env file
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
assert BASE_URL, "BASE_URL is not set in the environment variables"
GITHUB_PAT_TOKEN = os.getenv("GITHUB_PAT_TOKEN")
assert GITHUB_PAT_TOKEN, "GITHUB_PAT_TOKEN is not set in the environment variables"
CLONE_DIRECTORY = os.getenv("CLONE_DIRECTORY")
assert CLONE_DIRECTORY, "CLONE_DIRECTORY is not set in the environment variables"
CONFIG_FILE = os.getenv("CONFIG_FILE")
assert CONFIG_FILE, "CONFIG_FILE is not set in the environment variables"

# Variables to be used and set during testing
TEMPLATE_REPOSITORY_OWNER = "ituthon"
TEMPLATE_REPOSITORY_NAME = "test_user_template"

COMPETITION_ID = None
COMPETITION_NAME = f"Competition-{randint(10000, 99999)}"
COMPETITION_TEMPLATE = "datathonai24" # not to be confused with the github template repository, this is internal templates

TEAM_NAME = f"Team-{randint(10000, 99999)}"
REPO_NAME = None

MEMBER_EMAIL = "ertugrul.a.senturk@gmail.com"
MEMBER_GITHUB_USERNAME = "erthium"
MEMBER_USERNAME = "erthium"
MEMBER_NAME = "Ertugrul Senturk"


def print_info(message, *args, **kwargs):
  print(f"\033[94m{message}\033[0m", *args, **kwargs)  # Blue text for info messages

def print_success(message, *args, **kwargs):
  print(f"\033[92m{message}\033[0m", *args, **kwargs)  # Green text for success messages

def print_warning(message, *args, **kwargs):
  print(f"\033[93m{message}\033[0m", *args, **kwargs)  # Yellow text for warning messages

def print_error(message, *args, **kwargs):
  print(f"\033[91m{message}\033[0m", *args, **kwargs)  # Red text for error messages


def create_and_start_competition():
  global COMPETITION_ID, REPO_NAME
  if COMPETITION_ID is not None:
    print_warning("A competition is already created. Please reset the state before creating a new one.")
    return

  response = requests.post(f"{BASE_URL}/template/sync")
  assert response.status_code == 200, f"Failed to sync templates: {response.text}"
  print_success("Templates synced successfully.")

  response = requests.post(
    f"{BASE_URL}/competition/create",
    json={
      "name": COMPETITION_NAME,
    }
  )
  assert response.status_code == 200, f"Failed to create competition: {response.text}"
  COMPETITION_ID = response.json().get("competitions_id")
  print_success(f"Competition created with ID: {COMPETITION_ID}")

  response = requests.put(
    f"{BASE_URL}/competition/configure",
    json={
      "competition_id": COMPETITION_ID,
      "template_name": COMPETITION_TEMPLATE,
    }
  )
  assert response.status_code == 200, f"Failed to configure competition: {response.text}"
  print_success(f"Competition configured with template: {COMPETITION_TEMPLATE}")

  response = requests.post(
    f"{BASE_URL}/competition/add_teams",
    json={
      "competition_id": COMPETITION_ID,
      "teams": [
        {
          "name": TEAM_NAME,
          "members": [
            {
              "email": MEMBER_EMAIL,
              "github_username": MEMBER_GITHUB_USERNAME,
              "username": MEMBER_USERNAME,
              "name": MEMBER_NAME,
            }
          ]
        }
      ]
    }
  )
  assert response.status_code == 200, f"Failed to add teams: {response.text}"
  print_success(f"Team '{TEAM_NAME}' added to competition '{COMPETITION_NAME}'.")

  response = requests.post(
    f"{BASE_URL}/competition/start",
    json={
      "competition_id": COMPETITION_ID,
      "template_repository_owner": TEMPLATE_REPOSITORY_OWNER,
      "template_repository_name": TEMPLATE_REPOSITORY_NAME,
    }
  )
  assert response.status_code == 200, f"Failed to start competition: {response.text}"
  REPO_NAME = f"{COMPETITION_NAME}-{TEAM_NAME}"
  print_success(f"Competition '{COMPETITION_NAME}' started with repository '{REPO_NAME}'.")


def clone_repository():
  if COMPETITION_ID is None:
    print_warning("No competition created yet. Please create a competition first.")
    return
  if REPO_NAME is None:
    print_warning("No repository created yet. Please create a competition first.")
    return
  if os.path.exists(f"{CLONE_DIRECTORY}/{REPO_NAME}"):
    print_warning(f"Repository {REPO_NAME} already exists in {CLONE_DIRECTORY}. Please remove it before cloning again.")
    return
  repo_url = f"https://{TEMPLATE_REPOSITORY_OWNER}:{GITHUB_PAT_TOKEN}@github.com/{TEMPLATE_REPOSITORY_OWNER}/{REPO_NAME}.git"
  git_clone_process = subprocess.run(
    ["git", "clone", repo_url],
    cwd=CLONE_DIRECTORY,
    check=True
  )
  if git_clone_process.returncode != 0:
    print_error(f"Failed to clone the repository {REPO_NAME}. Please check the repository URL and your permissions.")
    return
  # Check if the repository was cloned successfully
  if not os.path.exists(f"{CLONE_DIRECTORY}/{REPO_NAME}"):
    print_error(f"Repository {REPO_NAME} was not cloned successfully. Please check the repository URL and your permissions.")
    return
  print_success(f"Repository {REPO_NAME} cloned successfully to {CLONE_DIRECTORY}/{REPO_NAME}.")


def make_random_submission():
  if COMPETITION_ID is None:
    print_warning("No competition created yet. Please create a competition first.")
    return
  if not os.path.exists(f"{CLONE_DIRECTORY}/{REPO_NAME}"):
    print_warning(f"Repository {REPO_NAME} not found in {CLONE_DIRECTORY}. Please clone the repository first.")
    return

  # First, pull the latest changes from the remote repository
  try:
    subprocess.run(
      ["git", "pull"],
      cwd=os.path.join(CLONE_DIRECTORY, REPO_NAME),
      check=True
    )
    print_info(f"Pulled the latest changes from the remote repository {REPO_NAME}.")
  except subprocess.CalledProcessError as e:
    print_error(f"Failed to pull the latest changes: {e}")
    return

  # Simulate making a random submission
  print_info(f"Making a random submission to {REPO_NAME}...")
  # Modify the README.md file in the cloned repository
  readme_path = os.path.join(CLONE_DIRECTORY, REPO_NAME, "README.md")
  if not os.path.exists(readme_path):
    print_error(f"README.md not found in {readme_path}. Please ensure the repository is cloned correctly.")
    return
  random_number = randint(10000, 99999)
  with open(readme_path, "a") as readme_file:
    readme_file.write(f"\n\nRandom submission at {random_number}\n")
  print_success(f"Random submission {random_number} made to {readme_path}.")
  # commit and push the changes
  try:
    subprocess.run(
      ["git", "add", "."],
      cwd=os.path.join(CLONE_DIRECTORY, REPO_NAME),
      check=True
    )
    print_info("Changes staged for commit.")
    subprocess.run(
      ["git", "commit", "-m", f"release: {random_number}"],
      cwd=os.path.join(CLONE_DIRECTORY, REPO_NAME),
      check=True
    )
    print_info(f"Changes committed with message: 'release: {random_number}'")
    subprocess.run(
      ["git", "push"],
      cwd=os.path.join(CLONE_DIRECTORY, REPO_NAME),
      check=True
    )
    print_success(f"Random submission {random_number} made successfully.")
  except subprocess.CalledProcessError as e:
    print_error(f"Failed to make a random submission: {e}")
    return
  except e:
    print_error(f"An unexpected error occurred: {e}")
    return


def remove_cloned_repository():
  global REPO_NAME, COMPETITION_ID
  if REPO_NAME is None:
    print_warning("No repository created yet. Please create a competition first.")
    return
  repo_path = os.path.join(CLONE_DIRECTORY, REPO_NAME)
  if not os.path.exists(repo_path):
    print_warning(f"Repository {REPO_NAME} not found in {CLONE_DIRECTORY}.")
    return
  try:
    print_warning(f"Are you sure you want to remove the repository on directory {repo_path}? (yes/no): ", end="")
    answer = input().strip().lower()
    if answer not in ["yes", "y"]:
      print_warning("Repository removal cancelled.")
      return
    subprocess.run(["rm", "-rf", repo_path], check=True)
    print_success(f"Repository {REPO_NAME} removed successfully from {CLONE_DIRECTORY}.")
    REPO_NAME = None
    COMPETITION_ID = None
  except subprocess.CalledProcessError as e:
    print_error(f"Failed to remove the repository {REPO_NAME}: {e}")


def show_current_status():
  # refresh the terminal, clear
  print("\033c", end="")
  print_info(f"Current Competition ID: {COMPETITION_ID}")
  # list all dirs in CLONE_DIRECTORY
  if os.path.exists(CLONE_DIRECTORY):
    print_info("Cloned repositories:")
    if len(os.listdir(CLONE_DIRECTORY)) == 1:
      print_warning("No repositories cloned yet.")
    else:
      for item in os.listdir(CLONE_DIRECTORY):
        if os.path.isdir(os.path.join(CLONE_DIRECTORY, item)):
          print_info(f"- {item}")
  print()


def save_config(COMPETITION_ID: str, REPO_NAME: str):
  config_data = {
    "COMPETITION_ID": COMPETITION_ID,
    "REPO_NAME": REPO_NAME,
  }
  with open(CONFIG_FILE, "w") as config_file:
    json.dump(config_data, config_file, indent=4)


def load_config():
  global COMPETITION_ID, REPO_NAME
  with open(CONFIG_FILE, "r") as config_file:
    config_data = json.load(config_file)
    COMPETITION_ID = config_data.get("COMPETITION_ID")
    REPO_NAME = config_data.get("REPO_NAME")


async def main():
  global COMPETITION_ID, REPO_NAME
  load_config()
  running = True
  while running:
    show_current_status()
    # 1 for create, 2 for clone, 3 for submit
    print_info("Choose an action:")
    print_info("1. Create and start a competition")
    print_info("2. Clone the repository")
    print_info("3. Make a random submission")
    print_info("4. Remove cloned repository")
    print_info("9. Exit")
    action = input("Enter your choice (1/2/3/4/9): ").strip().lower()
    if action == "1":
      create_and_start_competition()
    elif action == "2":
      clone_repository()
    elif action == "3":
      make_random_submission()
    elif action == "4":
      remove_cloned_repository()
    elif action == "quit" or action == "exit" or action == "q" or action == "9":
      print_info("Exiting the script.")
      running = False
    else:
      print_warning("Invalid action. Please choose 'create', 'clone', or 'submit'.")
    if running:
      save_config(COMPETITION_ID, REPO_NAME)
      input("Press Enter to continue...")  # Wait for user input before refreshing the status


if __name__ == "__main__":
  import asyncio
  asyncio.run(main())