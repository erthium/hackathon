from dataclasses import dataclass
from typing import List

from app.objects.template import Template


@dataclass
class GetAllTemplatesResponse:
  templates: List[Template]
