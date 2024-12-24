# Hackathon Platform Engine

This is the engine that is expected to test and evaluate teams' agents.

It has a CLI backed by the [Typer](https://typer.tiangolo.com/) ([repo](https://github.com/fastapi/typer)) package.

## To run

```bash
# Install requirements
pip install -r requirements.txt

# See available commands
python main.py --help

# Run the test command
python main.py test <repo owner> <repo name> <release tag>

# E.g.
python main.py test ituai-deneme deneme2 1.0.6
```
