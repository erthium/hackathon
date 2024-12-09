# Backend of Hackathon Platform with ITU AI Club

Backend notes are for the Hackathon Platform of ITU AI Club.

## Tech Stack

- **Environment:** Python 3.12 with FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Backend Deployment:** AWS EC2
- **Database Deployment:** AWS RDS


## Project Structure

There will be a frontend and an isolated game engine apart from the backend. The backend will always be in the middle of these two.

We do not desire to have much profiling for the users. Every comptetion the teams and users will be created from scratch. After the forms are filled the teams are accepted, we create their team and user information in the database, and send them an invitation email with a code. They will create their accounts with the code through the frontend. We will not hold any unnecessary data about the users.

Entire competition system will derive from the release commits of the teams. Every time there is commit starts with `release` tag, our backend will catch it through GitHub Webhook, and will ping the game engine to run the new release to see if it is valid.

After the competition ends, we will manually ping the game engine to run the final releases of all teams, and the winner will be decided.


## Database Structure

We will use PostgreSQL as the database, publish on AWS RDS, will be updated/migrated with Alembic.

**Team information:**
- Team ID: UUID, Unique
- Competition ID: UUID, Foreign Key
- Team Name: Predecided before invitation, unique for each competition
- GitHub Repository: Unique
- Current Member Count: Integer
- Expected Member Count: Integer
- Registration Date (UTC)

**User information:**
- User ID: UUID, Unique
- Team ID: UUID, Foreign Key
- GitHub Username: Unique
- Email: Unique for each competition
- Username: Unique for each competition
- Name
- Registration Date (UTC)

**Release information:**
- Release ID: UUID, Unique
- Commit ID
- Status: Pending, Approved, Rejected
- Message: Reason for rejection
- Release Date (UTC)

**Competition information:**
- Competition ID: UUID, Unique
- Competition Name: Unique
- Start Date (UTC)
- End Date (UTC)
- Status: Upcoming, Open, Ongoing, Completed
- Winner Team ID: UUID, Nullable, Foreign Key

**Invitation information:**
- Invitation Code: UUID, Unique
- Team ID: UUID, Foreign Key
- GitHub Username
- Email
- Invitation Email Status: Hasn't Sent, Sent, Had Error
- Registration Date (UTC)
- Expiration Date (UTC)
- Status: Active, Expired, Used

## User Reachable Endpoint Structure

For the user reachable endpoints, we will use JWT token for authentication. The token will be sent in the header as `Authorization Bearer {token}`.

User ID will be obtained from the token and will be used to get the team ID and other information.


### Authentication

Prefix: `/auth`

POST `/register`: Register with email, password, name, surname, and invitation code. Returns JWT token

POST `/login`: Login with email and password, returns JWT token

POST `/logout`: Logout, requires JWT token


### Team

Prefix: `/team`

GET `/{team_id}`: Get team information


### User

Prefix: `/user`

GET `/profile`: Get user profile


### Team Release

Prefix: `/release`

GET `/all`: Get all released agents

GET `/{commit_id}`: Get a release by commit ID, will be necessary when release check is still ongoing

POST `/select`: Select a release for the competition, requires commit ID of the release

DELETE `/delete/{commit_id}`: Delete a release by commit ID

GET `/status`: Returns the status to create a new release, has the information of time until another release can be created, if the team cannot create a new release, their commit will ignored


### Competition

Prefix: `/competition`

GET `/{competition_id}`: Get competition information


## Admin Reachable Endpoint Structure

### Team

Prefix: `/team`

GET `/all/{competition_id}`: Get all teams in a competition

POST `/create`: Create a team with a team name, competition ID and expected member count

POST `/update`: Update team information


### User

Prefix: `/user`

GET `/all/{team_id}`: Get all users in a team


### Release

Prefix: `/release`

GET `/all/{team_id}`: Get all releases of a team

POST `/approve`: Approve a release

POST `/reject`: Reject a release


### Competition

Prefix: `/competition`

GET `/all`: Get all competitions

POST `/create`: Create a competition

POST `/update`: Update competition information

POST `/lock/and/load`: Send all releases to the game engine to run. This will be manually called after the competition ends, game engine will decide the winner and ping the backend at the end

### Invitation

Prefix: `/invitation`

GET `/all/{team_id}`: Get all invitations of a team

POST `/create`: Create an invitation for a member

POST `/update`: Update invitation information

POST `/send`: Send an invitation to a member, take invitation code as input in the body

POST `/send/all`: Send all invitations in a competition, take competition ID as input in the body


## Automation Reachable Endpoint Structure

### Release

Prefix: `/release`

POST `/receive`: Receive a new release, this will be called by the GitHub Webhook

POST `/update`: Update a release, this will be called by the game engine after the release is checked


### Competition

Prefix: `/competition`

POST `/the/end`: End a competition, this will be called by the game engine after the competition ends


## Security Measures

- JWT token for user authentication, `https-only` cookies will expire in every 6 hours
- Passwords will be hashed with `bcrypt`
- Pydantic models will be used for request and response validation
- Database operations will be done with SQLAlchemy ORM to prevent any injection attacks
- All endpoints will be protected with CORS and CSRF protection with `fastapi.middleware.cors` and `fastapi.middleware.csrf`
- Rate limiting will be applied to all endpoints with `fastapi-limiter`
- Entire backend will have a firewall with `fastapi.middleware.trustedhost` and `fastapi.middleware.httpsredirect`
- Every important operation will be logged
- All logs will be sent to the Sentry with `sentry-sdk`
- All exceptions will be caught and sent to the Sentry
- Enpodint will always send a trimmed response, no unnecessary data will be sent
