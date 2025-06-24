# Templates

This directory contains the templates for the competition.

Templates are the main component of a competition that define all of the technical bits. The entire evaluation and submision logic is defined in the templates.

## Configuration

Every template has a `config.yaml` file that defines the configurations.

Here is a sample configuration:

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

### Fields

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
