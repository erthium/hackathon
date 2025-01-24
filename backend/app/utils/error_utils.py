from fastapi import HTTPException, status

from app.core.settings import app_settings

class ErrorUtils:

  @staticmethod
  def toHTTPException(exception: Exception) -> HTTPException:
    if isinstance(exception, HTTPException):
        return exception
    if app_settings.DEBUG:
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(exception))
    return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")
