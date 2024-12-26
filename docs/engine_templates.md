# Templates to be Used in the Engine

The entire platform will rely on the templates provided by the competition host. These templates will define:
- The structure of the code
- How the engine will run the code
- How the engine will evaluate the code

Before creating the competition, the host will either choose from the available templates or create a new one.

The templates in general will have 2 scripts in their core:
- Sandbox script: This script will run the code in a sandbox environment, to see if the submission is valid.
- Evaluation script: This script will evaluate the submission and determine the winner.

The templates will be stored in the database and will be used by the engine to run the code.


## Single Player Competition Template

In single player competitions, the sandbox script will also be responsible to test with the public data. The evaluation script will be responsible to test with the private data.

The both scripts will be getting input path for the cloned repository to run.


## Multi Player Competition Template

In multi player competitions, the sandbox script will only be responsible to test if the submission is valid and working in our server. The evaluation script will be responsible to necessary amount of input paths of different submissions to run and evaluate the results.

