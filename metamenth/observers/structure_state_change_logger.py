from metamenth.observers.interfaces.observer import Observer
from metamenth.datatypes.observable_message import ObservableMessage
from dataclasses import asdict


class StructureStateChangeLogger(Observer):
    """
    State logger for structure entities
    """

    def __init__(self):
        self._state_log: [ObservableMessage] = []

    def log_state(self, message: ObservableMessage):
        self._state_log.append(asdict(message))

    @property
    def state_log(self):
        return self._state_log
