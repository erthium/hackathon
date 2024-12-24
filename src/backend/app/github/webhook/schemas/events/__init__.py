from typing import TypeAlias

from .push import PushEvent
from .release import ReleaseEvent
from .repository import RepositoryEvent

WebhookEvent: TypeAlias = RepositoryEvent | PushEvent | ReleaseEvent
