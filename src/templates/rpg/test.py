import os

from libs.test_agent import TestAgent
from libs.base_agent import BaseAgent
from libs.game import GameEngine
from libs.dynamic_import import import_attribute


def test_the_agent(agent_repo: str):
  path_to_agent = os.path.join(agent_repo, "src")
  module_name = "agent"
  attribute_name = "Agent"
  Agent: BaseAgent = import_attribute(path_to_agent, module_name, attribute_name)
  #seed = "ituai"
  agent = Agent(name="SupposedlyContestantAgent")
  test_agent = TestAgent("TestAgent")
  engine = GameEngine(agent_a=agent, agent_b=test_agent)
  engine.start()


def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--agent-repo", type=str, required=True)
  args = parser.parse_args()
  test_the_agent(args.agent_repo)
