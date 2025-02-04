from typing import List

from app.objects.release.release_info import ReleaseInfo
from pydantic import BaseModel


class GetAllResponse(BaseModel):
  releases: List[ReleaseInfo]
