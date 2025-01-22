# Hackathon Platform Engine

This is the engine that is expected to test and evaluate teams' agents.

It has a REST API to communicate with the backend.

## To run

```bash
# Install requirements
pip install -r requirements.txt

# Run in dev mode (auto reload enabled)
# The backends uses the default port of 8000, so we attach this service to port 8001
fastapi dev --port 8001
```
