# Template System

The main platform is designed to be as competition agnostic as possible. At any point, the platform does not have any idea what the competition is about or what will be run to evaluate the submissions.

The template system allows organizers to create a competition template that defines the rules, evaluation scripts, and scoring metrics.

## Template Structure

The template is mainly a set of rules and definitions in a YAML file, which tells the engine how to run the competition, what commands to execute, and how the results should be scored.

Mainly, the template expects a command to run when a submission is made. This is not mandatory but the current structure is expected to be working with on-submission command that either validates the submission code or gets the public score of the submission.

A sample agent-based game environment template:

```yaml
name: rpg
description: A template for RPG games
version: 0.0.1
author: itu-ai
user_template_dir: user_template
commands:
  test:
    description: Checking if the submission works correctly
    usage: test <path-to-repo>
    execute: test.py
    arg_type: SENDER_REPO
    allocated_ram: 1024
    allocated_v_ram: 1024
    allocated_cpu: 1
    timeout: 60
  evaluate:
    description: Finalising the competition and evaluating the submissions according to the rules
    usage: evaluate +<path-to-repo>
    execute: evaluate.py
    arg_type: ALL_REPOS
    allocated_ram: 1024
    allocated_v_ram: 1024
    allocated_cpu: 1
    timeout: 60
on_submission_command: test
on_competition_end_command: evaluate
score_metrics:
  elo:
    description: Elo rating of the player
    is_ascending: false
    is_primary: true 
    is_public: true
    min_value: 0
    max_value: null
```

For more prediction based competitions, the template can be as simple as:

```yaml
name: datathonai24
description: A template for the past DatathonAI'24 competition
version: 0.0.1
author: itu-ai
user_template_dir: user_template
commands:
  evaluate:
    description: Evaluating a single repository
    usage: evaluate <path-to-repo>
    execute: evaluate.py
    arg_type: SENDER_REPO
    allocated_ram: 1024
    allocated_v_ram: 1024
    allocated_cpu: 1
    timeout: 60
on_submission_command: evaluate
on_competition_end_command: null
score_metrics:
  rmse_haversine_public:
    description: Root Mean Square Error of Haversine distance on the public test set
    is_ascending: true
    is_primary: true
    is_public: true
    min_value: 0
    max_value: null
  rmse_haversine_private:
    description: Root Mean Square Error of Haversine distance on the private test set
    is_ascending: true
    is_primary: true
    is_public: false
    min_value: 0
    max_value: null
```

### Template Configuration Fields

- `name`: The name of the template.
- `description`: A short description of the template.
- `version`: The version of the template.
- `author`: The author of the template.
- `user_template_dir`: The directory where the user template will be stored inside the template directory. The contents of this directory will be copied to the user's repository.
- `commands`: A dictionary of commands that can be executed in the template.
  - `description`: A short description of the command.
  - `usage`: How the command is used, used to describe the command for the developer/organiser.
  - `execute`: The script that will be executed when the command is run.
  - `arg_type`: The type of argument that the command accepts. Describes the arguments that the execute script will receive. It can be one of the following:
    - `SENDER_REPO`: The path to the sender's repository.
    - `ALL_REPOS`: The path to all repositories.
  - `allocated_ram`: The amount of RAM allocated for the command in MB.
  - `allocated_v_ram`: The amount of virtual RAM allocated for the command in MB.
  - `allocated_cpu`: The number of CPU cores allocated for the command.
  - `timeout`: The timeout for the command in seconds.
- `on_submission_command`: The command that will be executed when a submission is made.
- `on_competition_end_command`: The command that will be executed when the competition ends
- `score_metrics`: A dictionary of score metrics that will be used to evaluate the submissions.
  - `description`: A short description of the score metric.
  - `is_ascending`: Whether a higher value is better or not.
  - `is_primary`: Whether this score metric is the primary score metric for the competition.
  - `is_public`: Whether this score metric is public or not.
  - `min_value`: The minimum value of the score metric.
  - `max_value`: The maximum value of the score metric. If null, there is no maximum value.


## Template Directory Structure

Below is the expected directory structure of a template:

```powershell
/template_dir
    /libs                 # libraries to be used in command execution scripts
        dynamic_import.py
        utils.py
    /user_template        # content inside here will be copied to the user's repository
        ...
    requirements.txt      # requirements to run the command execution scripts
    config.yaml           # configuration file for the template
    on_submission.py      # command execution script
    on_competition_end.py # command execution script
```


And here is how an agent-based template's repository structure would look like:

```powershell
/user_template
    /src
        /libs             # libraries provided by the template, not to be modified by the user
            base_agent.py
        agent.py          # the main agent class that will be run
    .gitignore
    README.md             # explaining how to use the template
```

According to the template, the organiser can add almost anything inside the template and user template directories. This includes a Dockerfile that will be build and run when the commands are executed. The template system is designed to be as flexible as possible, allowing organizers to create any type of competition they want.


## Working with Large Datasets (TODO)

One thing that is not clearly solved yet is working with large datasets.

Since the template code will run on a virtual machine in cloud, putting the dataset inside the Docker image is not a good idea, since it will increase the size of the image and make it harder to work with.

Another idea is to put the dataset in cloud somewhere as well, to be installed in the Docker image at runtime, yet this would require an authentication process and it may not be a great idea to put a key/secret in the Docker image that we are saying will be isolated and running a code that is not trusted.
