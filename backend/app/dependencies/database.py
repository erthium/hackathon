from typing import Annotated

from app.core.db import get_database
from fastapi import Depends
from sqlalchemy.orm import Session

# Session is SessionLocal's (and get_database's) return type
database_dep = Annotated[Session, Depends(get_database)]
