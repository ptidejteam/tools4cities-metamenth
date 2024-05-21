from enumerations import MeasurementUnit
import uuid
from datatypes.schedulable_entity import SchedulableEntity


class AbstractEnergySystem:
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit):
        self._UID = str(uuid.uuid4())
        self._name = None
        self._inverter = None
        self._unit = None
        self._model = None
        self._manufacturer = None
        self._manufacturing_year = None
        self._schedulable_entity = SchedulableEntity()

        self.name = name
        self.inverter = inverter
        self.unit = unit

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
    def inverter(self) -> bool:
        return self._inverter

    @inverter.setter
    def inverter(self, value: bool):
        if value is None:
            raise ValueError("inverter should be of type bool")
        self._inverter = value

    @property
    def unit(self) -> MeasurementUnit:
        return self._unit

    @unit.setter
    def unit(self, value: MeasurementUnit):
        if value is None:
            raise ValueError("unit should be of type MeasurementUnit")
        self._unit = value

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str):
        if value is None:
            raise ValueError("model should be of type str")
        self._model = value

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value: str):
        if value is None:
            raise ValueError("manufacturer should be of type str")
        self._manufacturer = value

    @property
    def manufacturing_year(self) -> int:
        return self._manufacturing_year

    @manufacturing_year.setter
    def manufacturing_year(self, value: int):
        if value is None:
            raise ValueError("manufacturing_year should be of type int")
        self._manufacturing_year = value

    @property
    def schedulable_entity(self) -> SchedulableEntity:
        return self._schedulable_entity

    @schedulable_entity.setter
    def schedulable_entity(self, value: SchedulableEntity):
        if value is None:
            raise ValueError("schedules should be of type SchedulableEntity")
        self._schedulable_entity = value

    def __eq__(self, other):
        if isinstance(other, AbstractEnergySystem):
            return self.name == other.name
        return False

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Name: {self.name}, "
            f"Inverter: {self.inverter}, "
            f"Unit: {self.unit}, "
            f"Model: {self.model}, "
            f"Manufacturer: {self.manufacturer}, "
            f"Manufacturing Year: {self.manufacturing_year}, "
            f"Operational Schedule: {self._schedulable_entity}, "
        )
