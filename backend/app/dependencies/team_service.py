from fastapi import Depends
from typing import Annotated

from app.services.team_service import TeamService, get_team_service


team_service_dep = Annotated[TeamService, Depends(get_team_service)]
