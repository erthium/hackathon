from datetime import datetime, timezone

from sqlalchemy import func


class TimeUtils:
  @staticmethod
  def get_datetime_now() -> datetime:
    """
    Get the current date and time.
    return:
        return datetime object
    """
    return datetime.now(timezone.utc)


  @staticmethod
  def get_datetime_today() -> datetime:
    """
    Get the current date with time set to midnight.
    return:
        return datetime object with time set to midnight
    """
    return datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)


  @staticmethod
  def sqlalchemy_datetime_now() -> datetime:
    """
    Get the current date and time in a format suitable for SQLAlchemy.
    return:
        return datetime object in UTC timezone
    """
    return func.timezone('UTC', func.now())


  @staticmethod
  def get_now_seconds() -> int:
    """
    Get the current timestamp in seconds.
    return:
        return int timestamp in seconds
    """
    return int(datetime.now(timezone.utc).timestamp())


  @staticmethod
  def get_now_miliseconds() -> int:
    """
    Converts the current timestamp to a milliseconds value.
    return:
        return int milliseconds value
    """
    return round(datetime.now(timezone.utc).timestamp() * 1000)
