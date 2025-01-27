from abc import ABC, abstractmethod
from typing import List

from libs.objects import Action, AgentState, Item


class BaseAgent(ABC):
  def __init__(self, name: str, seed: int | None = None):
    self.name = name
    self.seed = seed

  @abstractmethod
  def prepare(self, initial_state: AgentState) -> List[Item]:
    """
    This method is called at the beginning of each fight to allow the agent to request items.
    The agent can request any number of items from the predefined items.
    The agent can request the same item multiple times if the item is stackable.
    The agent can request items with a total cost less than or equal to the initial money.
    :param initial_state: AgentState
    :return: List[Item]
    """
    pass

  @abstractmethod
  def act(
    self, agent_state: AgentState, opponent_state: AgentState, turn: int
  ) -> Action:
    """
    This method is called each time the agent needs to make a decision.
    The agent should return an action to perform.
    :param game_state: GameState
    :return: Action
    """
    pass
