from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime
from enumerations import TriggerType


@dataclass
class TriggerHistory:
    value: float
    trigger_type: TriggerType
    UID: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = datetime.now()
