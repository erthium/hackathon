"""
This is the main script the competitiors will be working on. This template expects you to fill the 'prepare' and 'act' methods with your own code.
- The 'prepare' method is called at the beginning of each fight to allow the agent to request items.
- The 'act' method is called each time the agent needs to make a decision. The agent should return an action to perform.

You can browse in the 'src/libs' directory to see the source code of the environment and the objects you can use in your agent.

The agent is initialized with a name and a seed.
Your agents name will be your team name, and seed will be defined before each fight.

You are not expected to create any instances of the agent class, the environment will do that for you.

You are free to use any external libraries you want, you can import them in the 'requirements.txt' file so they will be available in the environment.
"""

from typing import List
from src.libs.base_agent import BaseAgent
from src.libs.objects import AgentState, Action, Item, ActionType


class Agent(BaseAgent):
  def __init__(self, name, seed):
      super().__init__(name, seed)

  def prepare(self, initial_state: AgentState) -> List[Item]:
    return []

  def act(self, agent_state: AgentState, opponent_state: AgentState, turn: int) -> Action:
    return Action(ActionType.SKIP, None)
