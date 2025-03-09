from dataclasses import dataclass

from app.objects.template import Template


@dataclass
class GetAllTemplatesResponse:
  templates: list[Template]
