from fastapi import Depends
from typing import Annotated

from app.core.db import get_database, SessionLocal

database = Annotated[SessionLocal, Depends(get_database)]
