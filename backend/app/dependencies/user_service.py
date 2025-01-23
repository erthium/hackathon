from fastapi import Depends
from typing import Annotated

from app.services.user_service import UserService, get_user_service


user_service_dep = Annotated[UserService, Depends(get_user_service)]
