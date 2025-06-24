from fastapi import Depends
from typing import Annotated

from app.services.template_service import TemplateService, get_template_service


TemplateServiceDep = Annotated[TemplateService, Depends(get_template_service)]
