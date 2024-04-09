from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from enumerations import AirVolumeType
from subsystem.hvac_components.duct import Damper
from typing import List
from typing import Union


class AirVolumeBox(AbstractHVACComponent):
    def __init__(self, name: str, air_volume_type: AirVolumeType, inlet_dampers: Union[None, List[Damper]],
                 has_heater: bool = False):
        """
        Models an air volume box in a built environment
        :param name: the unique name of the air volume box
        :param inlet_dampers: inlet dampers that may be in the air volume boxes
        :param has_heater: indicates if the air volume box has heaters installed
        """
        super().__init__(name)
        self._air_volume_type = None
        self._inlet_dampers = inlet_dampers
        self._has_heater = has_heater

        self.air_volume_type = air_volume_type

    @property
    def air_volume_type(self) -> AirVolumeType:
        return self._air_volume_type

    @air_volume_type.setter
    def air_volume_type(self, value: AirVolumeType):
        if not value:
            raise ValueError("air_volume_type must be of type AirVolumeType")
        self._pump_type = value

    @property
    def has_heater(self) -> bool:
        return self._has_heater

    @has_heater.setter
    def has_heater(self, value: bool):
       self._has_heater = value

    @property
    def inlet_dampers(self) -> [Damper]:
        return self._inlet_dampers

    @inlet_dampers.setter
    def inlet_dampers(self, value: [Damper]):
        self._inlet_dampers = value

    def __str__(self):
        return (
            f"AirVolumeBox ({super().__str__()}"
            f"Air Volume Type: {self.air_volume_type.value}, "
            f"Inlet Dampers: {self.inlet_dampers}"
            f"Has Heater: {self.has_heater})"
        )
