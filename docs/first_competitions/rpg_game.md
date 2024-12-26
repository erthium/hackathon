# General Notes of RPG Game for Hackathon with ITU AI Club

Since it will be an event mainly for fun, we want to be inclusive and use `Python3` to make it easier for everyone to participate.

## Game Idea and Agents

The game will be a turn-based simple RPG game. Agents will select their stats and items in the beginning, and then during the match with other agents, they will decide which action to take in each turn.

In the beginning on the comptetion, `Agent` interface will be shared with the competitors. This interface will require them to write 2 functions:
- `prepare(money: int):` This function will be called in the beginning of every match:
  - It will take `money` as input
  - There will be 15 stat points to select (will be decided later)
  - Function will return a serilazible object like `JSON`, containing the stats and the items, to be processed by the game engine
- `action(state: object):` This function will be called in every turn of the match:
  - It will take `state` as input, explaning the current state of the game and the opponent
  - It will return the action (will be decided later) to be taken in that turn
