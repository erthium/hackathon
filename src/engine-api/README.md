# Hackathon Platform Engine API

This establishes the communication with the engine via HTTP. It runs the engine with its CLI.

## To run

```bash
# Install requirements
pip install -r requirements.txt

# Run in dev mode (auto reload enabled)
# The backends uses the default port of 8000, so we attach this service to port 8001
fastapi dev --port 8001
```
