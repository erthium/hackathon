from fastapi import Depends
from typing import Annotated

from app.services.competition_service import CompetitionService, get_competition_service


CompetitionServiceDep = Annotated[CompetitionService, Depends(get_competition_service)]
