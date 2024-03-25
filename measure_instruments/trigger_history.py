from dataclasses import field
from uuid import uuid4
from datetime import datetime
from enumerations import TriggerType
from misc import Validate


class TriggerHistory:

    def __init__(self, trigger_type: TriggerType, value: float = None, timestamp: str = None):
        self.trigger_type = trigger_type
        self.value = value
        self.UID = field(default_factory=lambda: str(uuid4()))
        self.timestamp: datetime = datetime.now().replace(microsecond=0) if timestamp is None \
            else Validate.parse_date(timestamp)

    def __eq__(self, other):
        if isinstance(other, TriggerHistory):
            return self.UID == other.UID
        return False
