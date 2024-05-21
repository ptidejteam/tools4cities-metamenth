from dataclasses import field
from uuid import uuid4
from datetime import datetime
from enumerations import TriggerType
from misc import Validate
from measure_instruments.interfaces.abstract_data_measure import AbstractDataMeasure


class TriggerHistory(AbstractDataMeasure):

    def __init__(self, trigger_type: TriggerType, value: float = None, timestamp: str = None):
        if value is None:
            value = 0.0
        super().__init__(value, timestamp)
        self.trigger_type = trigger_type

    def __eq__(self, other):
        if isinstance(other, TriggerHistory):
            return self.UID == other.UID
        return False
