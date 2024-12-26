# Competition Types The Platform Will Support

Essentially there are 2 different types of competitions that we want to be able to host on the platform.
### Single Player Competitions

These are competitions where a single player competes against a benchmark. The player submits their code, we run it on our servers and evaluate the predictions. The platform determines the winner based on the evaluation.

This type of competition requires a template as follows:
```
/project_dir
    /src
        main.py
    /input
        train.csv
        test.csv
        ...
    /output
        predictions.csv
    requirements.txt
    config.json
```

The `main.py` file should be where our platform will run the code.

The `input` directory should contain all the data files required for the competition.

The `output` directory should contain the predictions file.

The `requirements.txt` file should contain all the dependencies required to run the code.

The `config.json` file should contain the configuration for running the code and other information.


### Multi Player Competitions

These are competitions where multiple players compete against each other. The players submit their code, we do not run but import the code and run it on our servers. The platform evaluates the predictions and determines the winner.

This is mostly for agent-based competitions where the players submit their agents and the agents compete against each other.

This type of competition requires a template as follows:
```
/project_dir
    /src
        /lib
            agent_base.py
        agent.py
    requirements.txt
    config.json
```

The `agent_base.py` file should contain the base abstract class for the agent.

The `agent.py` file should contain the agent class that inherits from the base class.

The `requirements.txt` file should contain all the dependencies required to run the code.

The `config.json` file should contain the configuration for running the code and other information.
