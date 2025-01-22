from dataclasses import dataclass, field
from enum import Enum
from typing import List


@dataclass
class ItemEffect:
  # Offensive Effects
  attack_boost: float = 0.0 # increases attack by this amount
  critical_chance: float = 0.0 # increases chance of landing a critical hit
  counter_attack_chance: float = 0.0 # increases chance of counter attacking
  double_attack_chance: float = 0.0 # increases chance of attacking twice
  steal_chance: float = 0.0 # increases chance of stealing item

  # Defensive Effects
  defense_boost: float = 0.0 # increases defense by this amount
  prevent_death_chance: float = 0.0 # increases chance of preventing death
  prevent_damage_chance: float = 0.0 # increases chance of preventing damage
  thorns: float = 0.0 # reflects a portion of damage back to attacker
  heal_percentage: float = 0.0 # heals the player by a percentage of damage taken
  heal: float = 0 # heals the player by this amount


@dataclass
class Item:
  name: str
  cost: int
  is_stackable: bool # whether the item can be stacked
  is_usable: bool # whether the item can be used, or is passive
  is_consumable: bool # whether the item is consumed after use
  effect: ItemEffect
  duration: int = 1 # how many turns the item lasts, -1 for infinite


class PredefinedItems:
  DAGGER = Item(
    name="dagger",
    cost=10,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(attack_boost=5)
  )

  PRETTY_SWORD = Item(
    name="pretty_sword",
    cost=20,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(attack_boost=10)
  )

  DEAD_KNIGHTS_SWORD = Item(
    name="dead_knights_sword",
    cost=50,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(attack_boost=20)
  )

  SILVER_SHIELD = Item(
    name="silver_shield",
    cost=30,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(defense_boost=5)
  )

  GOLDEN_SHIELD = Item(
    name="golden_shield",
    cost=50,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(defense_boost=10)
  )

  HEALING_POTION = Item(
    name="healing_potion",
    cost=20,
    is_stackable=True,
    is_consumable=True,
    is_usable=True,
    effect=ItemEffect(heal=20)
  )

  REVIVE_POTION = Item(
    name="revive_potion",
    cost=50,
    is_stackable=True,
    is_consumable=True,
    is_usable=True,
    effect=ItemEffect(prevent_death_chance=1.0)
  )

  FIRE_BLESSED_HELMET = Item(
    name="fire_blessed_helmet",
    cost=30,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(prevent_damage_chance=0.2)
  )

  THE_ONE_RING = Item(
    name="the_one_ring",
    cost=100,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(attack_boost=30, defense_boost=30, prevent_death_chance=0.2)
  )

  FILTHY_MAGIC_WAND = Item(
    name="filthy_magic_wand",
    cost=50,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(critical_chance=0.2)
  )

  ARTHURS_KEYBOARD = Item(
    name="arthurs_keyboard",
    cost=100,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(double_attack_chance=0.2)
  )

  ALMOND_CROISSANT = Item(
    name="almond_croissant",
    cost=10,
    is_stackable=True,
    is_consumable=True,
    is_usable=True,
    effect=ItemEffect(heal=10)
  )

  LOKUM = Item(
    name="lokum",
    cost=5,
    is_stackable=True,
    is_consumable=True,
    is_usable=True,
    effect=ItemEffect(heal=5)
  )

  THINKPAD_X1 = Item(
    name="thinkpad_x1",
    cost=200,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(attack_boost=50)
  )

  NOKIA_33_10 = Item(
    name="nokia_33_10",
    cost=200,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(attack_boost=50, critical_chance=0.5)
  )

  COFFEE = Item(
    name="coffee",
    cost=5,
    is_stackable=True,
    is_consumable=True,
    is_usable=True,
    effect=ItemEffect(attack_boost=5, heal=5)
  )

  TYSONS_GLOVES = Item(
    name="tysons_gloves",
    cost=100,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(attack_boost=20, counter_attack_chance=0.3)
  )

  POTTERS_CLOCK = Item(
    name="potters_clock",
    cost=100,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(double_attack_chance=0.2, steal_chance=0.2)
  )

  BACK_TO_THE_FUTURE = Item(
    name="back_to_the_future",
    cost=250,
    is_stackable=False,
    is_consumable=False,
    is_usable=False,
    effect=ItemEffect(prevent_death_chance=0.7)
  )

  ADAMS_APPLE = Item(
    name="adams_apple",
    cost=100,
    is_stackable=True,
    is_consumable=True,
    is_usable=True,
    effect=ItemEffect(heal_percentage=1.0)
  )

  ALL_ITEMS = {
    item.name: item
    for item in [
      DAGGER, PRETTY_SWORD, DEAD_KNIGHTS_SWORD, SILVER_SHIELD, GOLDEN_SHIELD,
      HEALING_POTION, REVIVE_POTION, FIRE_BLESSED_HELMET, THE_ONE_RING,
      FILTHY_MAGIC_WAND, ARTHURS_KEYBOARD, ALMOND_CROISSANT, LOKUM,
      THINKPAD_X1, NOKIA_33_10, COFFEE, TYSONS_GLOVES, POTTERS_CLOCK,
      BACK_TO_THE_FUTURE, ADAMS_APPLE
    ]
  }

# Enums and Constants
class ActionType(Enum):
  ATTACK = "attack"
  STEAL = "steal"
  DEFEND = "defend"
  SKIP = "skip"


@dataclass
class Action:
  action_type: ActionType
  used_item: Item | None = None

SKIP_ACTION = Action(ActionType.SKIP)


@dataclass
class AgentState:
  # Base Stats
  name: str
  max_health: float = 100
  health: float = 100
  base_attack: float = 10
  base_defense: float = 5
  base_steal_chance: float = 0.4

  # Pre-battle Stats
  money: int = 100

  # Offensive Stats
  attack: int = 10
  critical_chance: float = 0.0
  counter_attack_chance: float = 0.0
  double_attack_chance: float = 0.0
  steal_chance: float = 0.4

  # Defensive Stats
  defense: float = 5
  prevent_death_chance: float = 0.0
  prevent_damage_chance: float = 0.0
  thorns: float = 0.0

  # Items
  items: List[Item] = field(default_factory=list)
  used_items: List[Item] = field(default_factory=list)


@dataclass
class Log:
  entries: List[str] = field(default_factory=list)

  def add_entry(self, entry: str):
    self.entries.append(entry)
    print(entry)
    

  def show_log(self):
    return "\n".join(self.entries)
