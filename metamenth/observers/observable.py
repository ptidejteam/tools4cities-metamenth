from metamenth.datatypes.observable_message import ObservableMessage


class Observable:
    """
    parent class for all entities that need
    their state to be tracked overtime
    """
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message: ObservableMessage):
        for observer in self._observers:
            observer.log_state(message)
