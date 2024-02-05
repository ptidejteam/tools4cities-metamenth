from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime
from enumerations import TriggerType


@dataclass
class TriggerHistory:
    trigger_type: TriggerType
    value: float = None
    UID: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = datetime.now()

    def __eq__(self, other):
        if isinstance(other, TriggerHistory):
            return self.UID == other.UID
        return False
