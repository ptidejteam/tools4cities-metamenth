from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.enumerations import CoilMaterial
from metamenth.enumerations import RefrigerantType
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure


class Condenser(AbstractHVACComponent):
    def __init__(self, name: str, refrigerant_type: RefrigerantType, coil_material: CoilMaterial,
                 heat_transfer_area: AbstractMeasure = None, heat_transfer_coefficient: float = 0.0):
        super().__init__(name)
        self._refrigerant_type = None
        self._coil_material = None
        self._heat_transfer_area = heat_transfer_area
        self._heat_transfer_coefficient = heat_transfer_coefficient

        self.refrigerant_type = refrigerant_type
        self.coil_material = coil_material

    @property
    def refrigerant_type(self) -> RefrigerantType:
        return self._refrigerant_type

    @refrigerant_type.setter
    def refrigerant_type(self, value: RefrigerantType):
        if not value:
            raise ValueError("refrigerant_type must be of type RefrigerantType")
        self._refrigerant_type = value

    @property
    def coil_material(self) -> CoilMaterial:
        return self._coil_material

    @coil_material.setter
    def coil_material(self, value: CoilMaterial):
        if not value:
            raise ValueError("coil_material must be of type CoilMaterial")
        self._coil_material = value

    @property
    def heat_transfer_area(self) -> AbstractMeasure:
        return self._heat_transfer_area

    @heat_transfer_area.setter
    def heat_transfer_area(self, value: AbstractMeasure):
        self._heat_transfer_area = value

    @property
    def heat_transfer_coefficient(self) -> float:
        return self._heat_transfer_coefficient

    @heat_transfer_coefficient.setter
    def heat_transfer_coefficient(self, value: float):
        self._heat_transfer_coefficient = value

    def calculate_heat_transfer_rate(self, temperature_difference: float) -> float:
        """
        computes the heat transfer rate of the condenser
        :param temperature_difference: the temperature difference
        :return:
        """
        if self._heat_transfer_area and self._heat_transfer_coefficient > 0.0:
            return self.heat_transfer_coefficient * self.heat_transfer_area.value * temperature_difference
        return 0.0
