from uuid import uuid4
from abc import ABC


class AbstractSubsystem(ABC):
    def __init__(self, name: str):
        """
        Defines parent class of all subsystems
        :param name:
        """
        self._UID = str(uuid4())
        self._name = None

        self.name = name

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value
        else:
            raise ValueError("name must be of type str")

    def __eq__(self, other):
        # subsystems are equal if they share the same name and UID
        if isinstance(other, AbstractSubsystem):
            # Check for equality based on the 'name' attribute
            return self.name == other.name
        return False

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Name: {self.name}"
        )
