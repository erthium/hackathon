from typing import Annotated

from app.core.db import SessionLocal, get_database
from fastapi import Depends

database_dep = Annotated[SessionLocal, Depends(get_database)]
