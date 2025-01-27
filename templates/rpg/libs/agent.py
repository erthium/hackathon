import random
from typing import List

from libs.base_agent import BaseAgent
from libs.objects import Action, ActionType, AgentState, Item, PredefinedItems


class Agent(BaseAgent):
  def prepare(self, initial_state: AgentState) -> List[Item]:
    requested_items: List[Item] = []

    # buy random items
    current_money = initial_state.money
    buyable_items = [item for item in PredefinedItems.ALL_ITEMS.values()]
    while current_money >= min(
      [item.cost for item in PredefinedItems.ALL_ITEMS.values()]
    ):
      for item in buyable_items:
        if random.random() > 0.5 and item.cost <= current_money:
          requested_items.append(item)
          current_money -= item.cost
          if not item.is_stackable:
            buyable_items.remove(item)

    return requested_items

  def act(
    self, agent_state: AgentState, opponent_state: AgentState, turn: int
  ) -> Action:
    # choose random action
    action_type = random.choice(list(ActionType))
    # for 50% of the time, use a random item
    usable_items = [item for item in agent_state.items if item.is_usable]
    used_item = (
      random.choice(usable_items)
      if random.random() > 0.5 and len(usable_items) > 0
      else None
    )
    return Action(action_type=action_type, used_item=used_item)
