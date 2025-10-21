# Command Run

After the template is properly configured, it is entirely up to the organizers to create the template commands that will be run when the commands are executed by the Engine.

Let's take an on-submission command as an example. After a submission is made, the Engine build and run the Docker image with the entire template and the repository of the team that made the submission.

After this point, we have the code to run, and a completely isolated environment to run it in.

If the template is for a prediction-based competition, the template knows exactly where to find the class/function that will be run to get the predictions.

...

## Some Clever Tricks

Let's think about a scenario for an agent-based competition. The teams will develop their agents, and at the end all of the agents will compete against each other.

Let's say there are 30 teams, each team will compete with every other team exactly once. This means that we will have `30 * 29 / 2 = 435` matches to run.

Since before every match, there will be a Docker image built for each team
