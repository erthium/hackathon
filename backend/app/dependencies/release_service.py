from fastapi import Depends
from typing import Annotated

from app.services.release_service import ReleaseService, get_release_service


release_service_dep = Annotated[ReleaseService, Depends(get_release_service)]
