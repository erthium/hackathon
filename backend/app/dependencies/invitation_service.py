from fastapi import Depends
from typing import Annotated

from app.services.invitation_service import InvitationService, get_invitation_service


invitation_service_dep = Annotated[InvitationService, Depends(get_invitation_service)]
