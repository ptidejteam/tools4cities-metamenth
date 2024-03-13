from abc import ABC
from uuid import uuid4
from transducers.interfaces.abstract_transducer import AbstractTransducer
from utils import EntityInsert
from enumerations import BuildingEntity
from utils import EntityRemover
from utils import StructureEntitySearch
from typing import Dict
from datatypes.interfaces.dynamic_entity import DynamicEntity


class AbstractSubsystem(DynamicEntity):
    def __init__(self, name: str):
        """
        Defines parent class of all subsystems
        :param name:
        """
        super().__init__()
        self._UID = str(uuid4())
        self._name = None

        self.name = name

    @property
    def UID(self) -> str:
        return self.UID

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
            return self.name == other.name and self.UID == other.UID
        return False

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Transducers: {self._transducers}"
        )
