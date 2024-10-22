import uuid
from metamenth.datatypes.schedulable_entity import SchedulableEntity
from metamenth.datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity
from metamenth.measure_instruments.meter import Meter


class AbstractCommonEnergySystem(AbstractDynamicEntity):
    def __init__(self, name: str):
        super().__init__()
        self._UID = str(uuid.uuid4())
        self._name = None
        self._model = None
        self._manufacturer = None
        self._meter = None
        self._schedulable_entity = SchedulableEntity()

        self.name = name

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is None:
            raise ValueError("name should be of type str")
        self._name = value

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str):
        self._model = value

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value: str):
        self._manufacturer = value

    @property
    def schedulable_entity(self) -> SchedulableEntity:
        return self._schedulable_entity

    @schedulable_entity.setter
    def schedulable_entity(self, value: SchedulableEntity):
        if value is None:
            raise ValueError("schedules should be of type SchedulableEntity")
        self._schedulable_entity = value

    @property
    def meter(self) -> Meter:
        return self._meter

    @meter.setter
    def meter(self, value: Meter):
        self._meter = value

    def __eq__(self, other):
        if isinstance(other, AbstractCommonEnergySystem):
            return self.name == other.name
        return False

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Manufacturer: {self.manufacturer}, "
            f"Manufacturing Year: {self.model}, "
            f"Meter: {self.meter}, "
            f"Operational Schedule: {self._schedulable_entity}, "
        )
