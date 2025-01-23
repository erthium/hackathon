from app.core.settings import app_settings
from fastapi import HTTPException, status


class ErrorUtils:
  @staticmethod
  def toHTTPException(exception: Exception) -> HTTPException:
    if isinstance(exception, HTTPException):
      return exception
    if app_settings.DEVELOPMENT:
      return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(exception))
    return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")
