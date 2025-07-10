import httpx
from fastapi import HTTPException, status

from app.logger import logger
from app.dependencies.database import DatabaseDep
from app.repositories import (
  TemplateRepository, get_template_repository,
  CommandRepository, get_command_repository,
  ScoreMetricRepository, get_score_metric_repository,
  CompetitionRepository, get_competition_repository,
)
from app.objects.template import GetAllTemplatesResponse, TemplateInfo, CommandInfo
from app.objects.message_response import MessageResponse
from app.objects.enums import RunCommandType
from app.entities import Template, Command, ScoreMetric
from app.core.settings import app_settings


class TemplateService:
  def __init__(self,
               template_repository: TemplateRepository,
               command_repository: CommandRepository,
               score_metric_repository: ScoreMetricRepository,
               competition_repository: CompetitionRepository,
              ):
    self.__template_repository = template_repository
    self.__command_repository = command_repository
    self.__score_metric_repository = score_metric_repository
    self.__competition_repository = competition_repository


  def get_command_from_type(self, template: Template, run_command_type: RunCommandType) -> Command:
    if run_command_type == RunCommandType.ON_SUBMISSION:
      on_submission_command_name = template.on_submission_command
      if on_submission_command_name is None:
        raise ValueError(f"Template {template.name} does not have an on_submission_command defined")
      command = self.__command_repository.get_by_name_and_template_id(
        name=on_submission_command_name,
        template_id=template.id
      )
      return command

    elif run_command_type == RunCommandType.ON_COMPETITION_END:
      on_competition_end_command_name = template.on_competition_end_command
      if on_competition_end_command_name is None:
        raise ValueError(f"Template {template.name} does not have an on_competition_end_command defined")
      command = self.__command_repository.get_by_name_and_template_id(
        name=on_competition_end_command_name,
        template_id=template.id
      )
      return command

    else:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Run commands other than ON_SUBMISSION and ON_COMPETITION_END are not supported yet"
      )


  def get_all(self) -> GetAllTemplatesResponse:
    all_templates = self.__template_repository.get_all()
    return GetAllTemplatesResponse(
      templates=[
        TemplateInfo.from_entity(template) for template in all_templates
      ]
    )
  
  def sync(self) -> MessageResponse:
    templates_from_engine = self._get_templates_from_engine()
    template_names_from_engine = {template["name"] for template in templates_from_engine}
    competitions_with_templates = self.__competition_repository.get_all_with_template_names()
    # Check if all template names used in competitions exist in the engine
    for competition_id, template_name in competitions_with_templates.items():
      if template_name not in template_names_from_engine:
        return HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"Template '{template_name}' used in competition {competition_id} does not exist in the engine"
        )
    self.__competition_repository.nullify_all_template_names()
    self._delete_all_templates()
    self._add_templates(templates_from_engine)
    self.__competition_repository.bring_back_template_names(competitions_with_templates)
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
    all_templates: dict = templates_response.get("templates", {})
    return all_templates


  def _delete_all_templates(self) -> None:
    self.__score_metric_repository.delete_all()
    self.__command_repository.delete_all()
    self.__template_repository.delete_all()


  def _add_templates(self, all_templates: dict) -> None:
    for template_info in all_templates:
      template = Template(
        name=template_info["name"],
        description=template_info["description"],
        author=template_info["author"],
        on_submission_command=template_info.get("on_submission_command", None),
        on_competition_end_command=template_info.get("on_competition_end_command", None),
      )
      self.__template_repository.save(template)

      for command_info in template_info["commands"]:
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

      for score_metric_info in template_info["score_metrics"]:
        score_metric = ScoreMetric(
          template_id=template.id,
          name=score_metric_info["name"],
          description=score_metric_info["description"],
          is_ascending=score_metric_info["is_ascending"],
          is_primary=score_metric_info["is_primary"],
          is_public=score_metric_info["is_public"],
          min_value=score_metric_info.get("min_value", None),
          max_value=score_metric_info.get("max_value", None),
        )
        self.__score_metric_repository.save(score_metric)


def get_template_service(db: DatabaseDep) -> TemplateService:
  return TemplateService(
    get_template_repository(db),
    get_command_repository(db),
    get_score_metric_repository(db),
    get_competition_repository(db),
  )
