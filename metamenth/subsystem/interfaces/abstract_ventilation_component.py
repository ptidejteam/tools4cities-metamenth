from uuid import uuid4
from typing import List
from metamenth.datatypes.continuous_measure import ContinuousMeasure
from metamenth.datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity


class AbstractVentilationComponent(AbstractDynamicEntity):

    def __init__(self, name: str):
        super().__init__()
        self._UID = str(uuid4())
        self._name = None
        self._operating_conditions: List[ContinuousMeasure] = []

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

    @property
    def operating_conditions(self) -> [ContinuousMeasure]:
        return self._operating_conditions.copy() if self._operating_conditions else []

    @operating_conditions.setter
    def operating_conditions(self, value: [ContinuousMeasure]):
        if value is not None and type(value) is list:
            self._operating_conditions.extend(value)

    def __eq__(self, other):
        # subsystems are equal if they share the same name
        if isinstance(other, AbstractVentilationComponent):
            # Check for equality based on the 'name' attribute
            return self.name == other.name and self.UID == other.UID
        return False

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Rated Device Measure: {self.operating_conditions}"
        )