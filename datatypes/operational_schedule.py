from datetime import datetime
from dataclasses import dataclass
from typing import Type
from datatypes.interfaces.abstract_measure import AbstractMeasure
from uuid import uuid4


@dataclass
class OperationalSchedule:
    UID = uuid4()
    name: str
    start_date: datetime
    end_date: datetime
    setPoint: Type[AbstractMeasure]
