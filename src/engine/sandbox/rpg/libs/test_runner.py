from game import GameEngine
from test_agent import TestAgent

# Example Usage
# seed: any = "ituai"
agent_a = TestAgent(name="AgentA")
agent_b = TestAgent(name="AgentB")
engine = GameEngine(agent_a=agent_a, agent_b=agent_b)
engine.start(initial_money=100)

"""
count = 10000
winner_a = 0
winner_b = 0
for _ in range(count):
  engine = GameEngine(agent_a=agent_a, agent_b=agent_b)
  engine.start(initial_money=0)
  is_winner_a = engine.agent_a_state.health > 0
  if is_winner_a:
    winner_a += 1
  else:
    winner_b += 1
print(f"Agent A wins {winner_a} times.")
print(f"Agent B wins {winner_b} times.")
"""
