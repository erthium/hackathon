from fastapi import Depends
from typing import Annotated

from app.services import CommandService, get_command_service


CommandServiceDep = Annotated[CommandService, Depends(get_command_service)]
