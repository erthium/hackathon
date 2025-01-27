import json
import os

from libs.base_agent import BaseAgent
from libs.dynamic_import import import_attribute
from libs.game import GameEngine
from libs.test_agent import TestAgent

RESULSTS_DIR = "/sandbox/results"


def test_the_agent(agent_repo: str):
  path_to_agent = os.path.join(agent_repo, "templates/rpg/libs")
  module_name = "agent.py"
  attribute_name = "Agent"

  os.makedirs(RESULSTS_DIR, exist_ok=True)
  with open(os.path.join(RESULSTS_DIR, "result.json"), "w") as f:
    try:
      Agent: BaseAgent = import_attribute(path_to_agent, module_name, attribute_name)
      # seed = "ituai"
      agent = Agent(name="SupposedlyContestantAgent")
      test_agent = TestAgent("TestAgent")
      engine = GameEngine(agent_a=agent, agent_b=test_agent)
      engine.start()
      f.write(json.dumps({"success": True, "result": engine.log.show_log()}))
    except Exception as e:
      f.write(json.dumps({"success": False, "error": str(e)}))


def main():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("--agent-repo", type=str, required=True)
  args = parser.parse_args()
  test_the_agent(args.agent_repo)


if __name__ == "__main__":
  main()
