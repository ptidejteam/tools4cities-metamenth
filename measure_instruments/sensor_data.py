from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime


@dataclass
class SensorData:
    value: float
    UID: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = datetime.now()

    def __eq__(self, other):
        if isinstance(other, SensorData):
            return self.UID == other.UID
        return False
