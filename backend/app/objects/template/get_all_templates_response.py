from dataclasses import dataclass

from app.objects.template import TemplateInfo


@dataclass
class GetAllTemplatesResponse:
  templates: list[TemplateInfo]
