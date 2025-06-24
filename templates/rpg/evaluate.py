from random import shuffle
from typing import List

from libs.base_agent import BaseAgent
from libs.game import GameEngine
from libs.utils import generate_seed, directory_checks, get_agent_from_repo


def arrange_fight(agent_a_repo: str, agent_b_repo: str):
  seed = generate_seed()

  # Shuffle the agents to avoid any bias
  agent_a_repo, agent_b_repo = shuffle([agent_a_repo, agent_b_repo])

  # Create the agents
  agent_a: BaseAgent = get_agent_from_repo(agent_a_repo, seed)
  agent_b: BaseAgent = get_agent_from_repo(agent_b_repo, seed)

  # Start the fight
  engine = GameEngine(agent_a=agent_a, agent_b=agent_b, seed=seed)
  engine.start()


def evaluate_agents(agent_repos: List[str]):
  for i, agent_a_repo in enumerate(agent_repos):
    for agent_b_repo in agent_repos[i+1:]:
      arrange_fight(agent_a_repo, agent_b_repo)


def main():
  import argparse
  parser = argparse.ArgumentParser()
  # parser will have number_of_repos as first argument, and the rest will be agent repos
  parser.add_argument('number_of_repos', type=int, help='The number of agent repos')
  parser.add_argument('agent_repos', type=str, nargs='+', help='The repositories of the agents')
  args = parser.parse_args()
  number_of_repos: int = args.number_of_repos
  agent_repos: List[str] = args.agent_repos
  assert len(agent_repos) == number_of_repos, 'Number of agent repositories in the first argument does not match the number of repositories provided'
  for repository in agent_repos:
    directory_checks(repository)
  evaluate_agents(agent_repos)
