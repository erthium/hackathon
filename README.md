# Hackathon Platform


## License

This project is licensed under the GNU GPL-3.0 license.


## Local Testing

The entire setup is dockerized, so you can run the project locally with Docker.

### Docker Helper

Mostly used commands for Docker & Docker Compose:

```shell
# Build the entire project, '-d' for detached mode, '--build' to rebuild the images
docker compose up -d --build

# Stop the project
docker compose down

# Stop the project and remove all volumes
docker compose down -v

# Watch the logs of the project
docker compose logs -f service_name
```

Since the GitHub Webhooks require a public domain, the easiest solution to test in local is to use ngrok with it's free static domain and have it pointing to your backend server.


## Conventions

**Branches**: `main` is the main branch, for the stable version of the project. `dev` is the development branch, where the new features are implemented.

For the branch names, use the following pattern: `type/description`. For example, `feature/login`, `fix/bug-in-register` or `docs/update-readme`.

**Commits**: We are using conventional commits. For more information, check [this site](https://www.conventionalcommits.org/en/v1.0.0/).

Basically, the commit message should be like this: `<type>[optional scope]: <description>`

Generaly used types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Pull Requests**: The PRs should be made to the `main` branch from the feature branck. The PRs should have a title and a description, explaining what was done and why.

**Python Syntax**: We are using PEP8 for the Python syntax. For more information, check [this site](https://peps.python.org/pep-0008/).

Basically we will use:
- camelCase for functions 
- snake_case for variables
- UpperCamelCase for classes
- UPPER_CASE for constants
- 2 spaces for indentation
