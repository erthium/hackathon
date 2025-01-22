# Hackathon Platform Backend

This service communicates with GitHub via [GitHub webhooks](https://docs.github.com/en/webhooks/about-webhooks) and [GitHub REST API](https://docs.github.com/en/rest?apiVersion=2022-11-28).

Webhooks notify the backend about changes on repositories (releases etc.) while the backend sends requests to the GitHub's REST API for creating repositories for teams etc.

## To run

```bash
# Install requirements
pip install -r requirements.txt

# Run in dev mode (auto reload enabled)
fastapi dev
```
