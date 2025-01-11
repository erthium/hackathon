from typing import List
import random

from objects import AgentState, Log, PredefinedItems, Action, ActionType, Item, SKIP_ACTION
from base_agent import BaseAgent


class GameEngine:
  def __init__(self, agent_a: BaseAgent, agent_b: BaseAgent, seed: int = None):
    self.agent_a: BaseAgent = agent_a
    self.agent_b: BaseAgent = agent_b

    self.agent_a_state = AgentState(name=self.agent_a.name)
    self.agent_b_state = AgentState(name=self.agent_b.name)

    self.seed = seed
    if seed is None:
      self.seed = random.randint(0, 1000000)
    random.seed(seed)

    self.log = Log()
    self.log.add_entry(f"Seed: {self.seed}")


  def roll_dice(self, max_value: float = 1.0) -> float:
    return random.random() * max_value


  def _validate_preparation(self, player: AgentState, requested_items: List[Item]):
    total_cost = 0
    checked_items = []
    for item in requested_items:

      if item.name not in PredefinedItems.ALL_ITEMS.keys():
        raise ValueError(f"{player.name} tried to buy an invalid item: {item.name}")

      if item.name in checked_items and not item.is_stackable:
        raise ValueError(f"{player.name} tried to buy a non-stackable item multiple times: {item.name}")

      total_cost += item.cost
      checked_items.append(item.name)

      if total_cost > player.money:
        raise ValueError(f"{player.name} tried to buy items exceeding their money.")

    self.log.add_entry(f"{player.name} bought items: {', '.join([item.name for item in requested_items])}.")


  def _validate_action(self, agent_state: AgentState, action: Action):
    if action.used_item is not None:
      if action.used_item not in agent_state.items:
        raise ValueError(f"{agent_state.name} tried to use an item they don't have.")


  def _apply_item_effects(self, agent_state: AgentState, item: Item) -> AgentState:
    # Offensive Effects
    agent_state.attack += item.effect.attack_boost
    agent_state.critical_chance = min(agent_state.critical_chance + item.effect.critical_chance, 1)
    agent_state.counter_attack_chance += min(agent_state.counter_attack_chance + item.effect.counter_attack_chance, 1)
    agent_state.double_attack_chance += min(agent_state.double_attack_chance + item.effect.double_attack_chance, 1)
    agent_state.steal_chance += min(agent_state.steal_chance + item.effect.steal_chance, 1)

    # Defensive Effects
    agent_state.defense += item.effect.defense_boost
    agent_state.prevent_death_chance += min(agent_state.prevent_death_chance + item.effect.prevent_death_chance, 1)
    agent_state.prevent_damage_chance += min(agent_state.prevent_damage_chance + item.effect.prevent_damage_chance, 1)
    agent_state.thorns += item.effect.thorns
    agent_state.health = min(agent_state.health + item.effect.heal_percentage * agent_state.max_health, agent_state.max_health)
    agent_state.health = min(agent_state.health + item.effect.heal, agent_state.max_health)

    return agent_state


  def _calculate_stats(self, agent_state: AgentState, action: Action) -> AgentState:
    agent_state.attack = agent_state.base_attack
    agent_state.defense = agent_state.base_defense
    agent_state.steal_chance = agent_state.base_steal_chance

    for item in agent_state.items:

      if item.is_usable:
        continue

      agent_state = self._apply_item_effects(agent_state, item)

    if action.action_type == ActionType.DEFEND:
      agent_state.defense *= 1.3

    if len(agent_state.used_items) > 0:
      for index in range(len(agent_state.used_items)):
        if agent_state.used_items[index].duration > 0:
          agent_state = self._apply_item_effects(agent_state, agent_state.used_items[index])
          agent_state.used_items[index].duration -= 1
      for index in range(len(agent_state.used_items)):
        if agent_state.used_items[index].duration == 0:
          agent_state.used_items.pop(index)

    return agent_state


  def prepare_agent(self, agent: BaseAgent, agent_state: AgentState):
    requested_items: List[Item] = agent.prepare(agent_state)
    self._validate_preparation(agent_state, requested_items)
    for item in requested_items:
      agent_state.items.append(item)
      agent_state.money -= item.cost


  def start(self, initial_money: int = 100):
    # Preparation Phase
    self.agent_a_state.money = initial_money
    self.agent_b_state.money = initial_money

    self.prepare_agent(self.agent_a, self.agent_a_state)
    self.prepare_agent(self.agent_b, self.agent_b_state)

    self.agent_a_state = self._calculate_stats(self.agent_a_state, SKIP_ACTION)
    self.agent_b_state = self._calculate_stats(self.agent_b_state, SKIP_ACTION)

    # Game Loop
    turn = 0
    while self.agent_a_state.health > 0 and self.agent_b_state.health > 0:
        agent = self.agent_a if turn % 2 == 0 else self.agent_b
        agent_state = self.agent_a_state if turn % 2 == 0 else self.agent_b_state
        opponent_state = self.agent_b_state if turn % 2 == 0 else self.agent_a_state

        action: Action = agent.act(
          agent_state=agent_state,
          opponent_state=opponent_state,
          turn=turn
        )

        self._validate_action(agent_state, action)

        # Calculate & Apply Action Result, Update Game State
        if action.used_item is not None:
          agent_state.used_items.append(action.used_item)
          agent_state.items.remove(action.used_item)
          agent_state = self._apply_item_effects(agent_state, action.used_item)
          self.log.add_entry(f"{agent.name} uses {action.used_item.name}.")

        if action.action_type == ActionType.ATTACK:
          opponent_counter_attack = self.roll_dice() < opponent_state.counter_attack_chance
          if opponent_counter_attack:
            opponent_critical_hit = 2.0 if self.roll_dice() < opponent_state.critical_chance else 1.0
            opponent_double_attack = 2 if self.roll_dice() < opponent_state.double_attack_chance else 1
            attack = opponent_state.attack * opponent_critical_hit * opponent_double_attack
            damage = max(attack - agent_state.defense, 1)
            agent_state.health -= damage
            self.log.add_entry(f"{opponent_state.name} counter attacks {agent.name} for {damage} damage.")

          else:
            critical_hit = 2.0 if self.roll_dice() < agent_state.critical_chance else 1.0
            double_attack = 2 if self.roll_dice() < agent_state.double_attack_chance else 1
            opponent_prevent_damage = 0.0 if self.roll_dice() < opponent_state.prevent_damage_chance else 1.0
            attack = agent_state.attack * critical_hit * double_attack * opponent_prevent_damage
            damage = max(attack - opponent_state.defense, 1)
            opponent_state.health -= damage
            self.log.add_entry(f"{agent.name} attacks {opponent_state.name} for {damage} damage.")

        elif action.action_type == ActionType.STEAL:
          if len(opponent_state.items) == 0:
            self.log.add_entry(f"{agent.name} tries to steal from {opponent_state.name} but they have no items.")
          else:
            if self.roll_dice() < agent_state.steal_chance:
              stolen_item = random.choice(opponent_state.items)
              opponent_state.items.remove(stolen_item)
              agent_state.items.append(stolen_item)
              self.log.add_entry(f"{agent.name} steals {stolen_item.name} from {opponent_state.name}.")
            else:
              self.log.add_entry(f"{agent.name} fails to steal from {opponent_state.name}.")

        elif action.action_type == ActionType.DEFEND:
          self.log.add_entry(f"{agent.name} defends.")

        elif action.action_type == ActionType.SKIP:
          self.log.add_entry(f"{agent.name} is a bystander.")


        if turn % 2 == 0:
          self.agent_a_state = self._calculate_stats(agent_state, action)
          self.agent_b_state = opponent_state
        else:
          self.agent_b_state = self._calculate_stats(agent_state, action)
          self.agent_a_state = opponent_state

        turn += 1

        print(f"Turn ended with {self.agent_a.name} having {self.agent_a_state.health} health and {self.agent_b.name} having {self.agent_b_state.health} health.")
        print(f"{self.agent_a.name} has following items: {", ".join([item.name for item in self.agent_a_state.items])}")
        print(f"{self.agent_b.name} has following items: {", ".join([item.name for item in self.agent_b_state.items])}")
        print("-" * 50)

    # Game Over
    winner: BaseAgent = self.agent_a_state if self.agent_a_state.health > 0 else self.agent_b_state
    self.log.add_entry(f"{winner.name} wins the fight!")
