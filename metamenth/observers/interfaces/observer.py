from abc import ABC
from abc import abstractmethod
from metamenth.datatypes.observable_message import ObservableMessage


# Observer interface
class Observer(ABC):
    """
    An interface that defines method to log state of entities
    that need their state to be tracked
    """
    @abstractmethod
    def log_state(self, message: ObservableMessage):
        """
        logs the state of an object
        :param message: object {entity_type, entity_id, state, message}
        :return:
        """
        pass
