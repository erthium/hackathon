# The Idea for the Project

The target is to be able to host programming competitions with as much flexibility as possible; where we can:
- Create any type of competition, be it prediction-based or agent-based
- Have the freedom to either share the entire dataset, or not share it at all
- Have the ability to run the submitted code in our own environment, with security checks included within when necessary


Even though there are many platforms that host such competitions, like Kaggle, Grand Challenge, AICrowd; they lack a few features that we need:
- We cannot run the submitted code in our own environment, competitors mostly submit their outputs, which means that if the competition is based on a dataset, we will have to share the private dataset with the competitors.
- If we wanted to create an agent-based competition, most platforms do not support it.

Some platforms offer such flexibilities, yet the organisers either have to pay or have to be eligible for a grant to use the platform; which takes time and requires a trusted organisation. Since we are a student club, we do not have both.

The idea of this project started about there, when we needed a system where we can go wild and implement any mechanic we want, for any type of competition, without any restrictions.


## The Main Competition Types


Essentially there are 2 different types of competitions that we want to be able to host on the platform.


## Mono-Competitor

These are competitions where a single team competes against a benchmark. The teams submit their code, we run it on our servers and evaluate the predictions. The platform determines the winner based on the evaluation.


## Multi-Competitor

These are competitions where multiple teams compete against each other. They submit their code, we do not run but import the code and run it on our servers. The platform evaluates the scores and determines the winner.

This is mostly for agent-based competitions where the players submit their agents and the agents compete against each other.
