from dataclasses import dataclass
from typing import Dict
from datetime import datetime


@dataclass
class ObservableMessage:
    entity_type: str
    entity_id: str
    state: Dict
    message: str = None
    timestamp = datetime.now()
