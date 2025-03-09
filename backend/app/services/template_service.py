import httpx
from fastapi import HTTPException, status

from app.dependencies import database_dep
from app.repositories import (
  TemplateRepository, get_template_repository,
  CommandRepository, get_command_repository,
)
from app.objects.template import GetAllTemplatesResponse, TemplateInfo, CommandInfo
from app.objects.message_response import MessageResponse
from app.entities import Template, Command
from app.core.settings import app_settings


class TemplateService:
  def __init__(self, template_repository: TemplateRepository, command_repository: CommandRepository):
    self.__template_repository = template_repository
    self.__command_repository = command_repository

  def get_all(self) -> GetAllTemplatesResponse:
    all_templates = self.__template_repository.get_all()
    return GetAllTemplatesResponse(
      templates=[
        TemplateInfo.from_entity(template) for template in all_templates
      ]
    )
  
  def sync(self) -> MessageResponse:
    templates_from_engine = self._get_templates_from_engine()
    self._delete_all_templates()
    self._add_templates(templates_from_engine)
    return MessageResponse(message=f"Templates synced successfully, {len(templates_from_engine)} templates found")

  def _get_templates_from_engine(self) -> None:
    template_endpoint = f"{app_settings.ENGINE_API_BASE_URL}/template/all"
    response = httpx.get(template_endpoint)
    if response.status_code != 200:
      raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Failed to fetch templates from engine, sync aborted"
      )
    templates_response: dict = response.json()
    print(templates_response)
    all_templates: dict = templates_response.get("templates", {})
    return all_templates

  def _delete_all_templates(self) -> None:
    self.__command_repository.delete_all()
    self.__template_repository.delete_all()

  def _add_templates(self, all_templates: dict) -> None:
    for template_info in all_templates:
      template = Template(
        name=template_info["name"],
        description=template_info["description"],
        author=template_info["author"],
      )
      self.__template_repository.save(template)
      all_commands: dict = template_info["commands"]
      for command_info in all_commands:
        command = Command(
          template_id=template.id,
          name=command_info["name"],
          description=command_info["description"],
          arg_type=command_info["arg_type"],
          allocated_ram=command_info["allocated_ram"],
          allocated_v_ram=command_info["allocated_v_ram"],
          allocated_cpu=command_info["allocated_cpu"],
          timeout=command_info.get("timeout", None),
        )
        self.__command_repository.save(command)


def get_template_service(db: database_dep) -> TemplateService:
  return TemplateService(get_template_repository(db), get_command_repository(db))
