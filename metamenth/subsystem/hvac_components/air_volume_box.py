from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from metamenth.enumerations import AirVolumeType
from metamenth.subsystem.hvac_components.duct import Damper
from metamenth.datatypes.binary_measure import BinaryMeasure


class AirVolumeBox(AbstractDuctConnectedComponent):
    def __init__(self, name: str, air_volume_type: AirVolumeType,
                 has_heating_capability: bool = False, has_cooling_capability: bool = False):
        """
        Models an air volume box in a built environment
        :param name: the unique name of the air volume box
        :param has_heating_capability: indicates if the air volume box can heat air
        :param has_cooling_capability: indicates if the air volume box can cool air
        """
        super().__init__(name)
        self._air_volume_type = None
        self._inlet_dampers: [Damper] = []
        self._has_heating_capability = has_heating_capability
        self._has_cooling_capability = has_cooling_capability
        self._max_air_flow = None

        self.air_volume_type = air_volume_type

    @property
    def air_volume_type(self) -> AirVolumeType:
        return self._air_volume_type

    @air_volume_type.setter
    def air_volume_type(self, value: AirVolumeType):
        if not value:
            raise ValueError("air_volume_type must be of type AirVolumeType")
        self._air_volume_type = value

    @property
    def has_heating_capability(self) -> bool:
        return self._has_heating_capability

    @has_heating_capability.setter
    def has_heating_capability(self, value: bool):
       self._has_heating_capability = value

    @property
    def has_cooling_capability(self) -> bool:
        return self._has_cooling_capability

    @has_cooling_capability.setter
    def has_cooling_capability(self, value: bool):
        self._has_cooling_capability = value

    @property
    def inlet_dampers(self) -> [Damper]:
        return self._inlet_dampers

    @inlet_dampers.setter
    def inlet_dampers(self, value: [Damper]):
        self._inlet_dampers = value

    @property
    def max_air_flow(self) -> BinaryMeasure:
        return self._max_air_flow

    @max_air_flow.setter
    def max_air_flow(self, value: BinaryMeasure):
        self._max_air_flow = value

    def __str__(self):
        return (
            f"AirVolumeBox ({super().__str__()}"
            f"Air Volume Type: {self.air_volume_type.value}, "
            f"Inlet Dampers: {self.inlet_dampers}, "
            f"Maximum Air Flow: {self.max_air_flow}, "
            f"Has Cooling Capability: {self._has_cooling_capability}, "
            f"Has Heating Capability: {self.has_heating_capability})"
        )
