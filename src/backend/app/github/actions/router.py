from fastapi import APIRouter

from ..api import add_webhook_to_repo, create_repo_in_org, invite_collaborators_to_repo
from .schemas import PrepareChallengePayload

router = APIRouter(prefix="/actions", tags=["actions"])


@router.post("/challenge/prepare")
async def prepare_challenge(challenge_data: PrepareChallengePayload):
    for teamIndex, team in enumerate(challenge_data.teams):
        repo_name = f"{challenge_data.challenge_name}-{team.team_name}-{str(teamIndex).rjust(3, '0')}"
        create_repo_in_org(
            "ituai-deneme",
            repo_name,
        )
        invite_collaborators_to_repo(
            "ituai-deneme",
            repo_name,
            team.team_members,
        )
        add_webhook_to_repo(
            "ituai-deneme",
            repo_name,
        )
