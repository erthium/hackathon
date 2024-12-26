# Engine of Hackathon Platform with ITU AI Club

Engine notes are for the Hackathon Platform of ITU AI Club.

## Tech Stack

- **Environment:** Python 3.12
- **Deployment:** Dockerised, in our own server
- **CI/CD:** GitHub Actions for testing, manual deployment

Main Engine will a Python module on its own, the communication with the backend will be through REST API with FastAPI.


## Project Structure

Engines main role will be to get the submission from the backend, then either run the code in a sandbox environment or run the code and evaluate the results.

Engine will get the repository, submission/commit tag and the template from the backend. Then it will:
- Clone the repository
- Run the sandbox or evaluation script with the cloned repository path
- Return the result of the sandbox script

The engine will not care about the template, the competition type, the input/output data or the evaluation metric. It will be the responsibility of the host to provide the correct template and the evaluation metric.
