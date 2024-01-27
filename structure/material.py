from enumerations import MaterialType
from datatypes.interfaces.abstract_measure import AbstractMeasure
import uuid
from misc import Validate


class Material:
    """
    Material making up layers in the envelope of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(
        self,
        description: str,
        material_type: MaterialType,
        density: AbstractMeasure,
        heat_capacity: AbstractMeasure,
        thermal_transmittance: AbstractMeasure,
        thermal_resistance: AbstractMeasure,
        solar_heat_gain_coefficient: float = None,
    ):
        Validate.validate_none({"description": description, "material_type": material_type,
                                "density": density, "heat_capacity": heat_capacity,
                                "thermal_transmittance": thermal_transmittance,
                                "thermal_resistance": thermal_resistance})
        self._UID = str(uuid.uuid4())
        self._description = description
        self._material_type = material_type
        self._density = density
        self._heat_capacity = heat_capacity
        self._thermal_transmittance = thermal_transmittance
        self._thermal_resistance = thermal_resistance
        self._solar_heat_gain_coefficient = Validate.validate_solar_heat_gain_coefficient(solar_heat_gain_coefficient)

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if value is None:
            raise ValueError("description must be a string")
        self._description = value

    @property
    def material_type(self) -> MaterialType:
        return self._material_type

    @material_type.setter
    def material_type(self, value: MaterialType):
        if value is None:
            raise ValueError("material_type must be of type MaterialType")
        self._material_type = value

    @property
    def density(self) -> AbstractMeasure:
        return self._density

    @density.setter
    def density(self, value: AbstractMeasure):
        if value is None:
            raise ValueError("density must be of type BinaryMeasure")
        self._density = value

    @property
    def heat_capacity(self) -> AbstractMeasure:
        return self._heat_capacity

    @heat_capacity.setter
    def heat_capacity(self, value: AbstractMeasure):
        if value is None:
            raise ValueError("heat_capacity must be of type BinaryMeasure")
        self._heat_capacity = value

    @property
    def thermal_transmittance(self) -> AbstractMeasure:
        return self._thermal_transmittance

    @thermal_transmittance.setter
    def thermal_transmittance(self, value: AbstractMeasure):
        if value is None:
            raise ValueError("thermal_transmittance must be of type BinaryMeasure")
        self._thermal_transmittance = value

    @property
    def thermal_resistance(self) -> AbstractMeasure:
        return self._thermal_resistance

    @thermal_resistance.setter
    def thermal_resistance(self, value: AbstractMeasure):
        if value is None:
            raise ValueError("thermal_resistance must be of type BinaryMeasure")
        self._thermal_resistance = value

    @property
    def solar_heat_gain_coefficient(self) -> float:
        return self._solar_heat_gain_coefficient

    @solar_heat_gain_coefficient.setter
    def solar_heat_gain_coefficient(self, value: float):
        self._solar_heat_gain_coefficient = Validate.validate_solar_heat_gain_coefficient(value)

    def __str__(self):
        return (
            f"Material("
            f"UID: {self.UID}, "
            f"Description: {self.description}, "
            f"Type: {self.material_type.value}, "
            f"Density: {self.density.value} {self.density.measurement_unit.value}, "
            f"Heat Capacity: {self.heat_capacity.value} {self.heat_capacity.measurement_unit.value}, "
            f"Thermal Transmittance: {self.thermal_transmittance.value} {self.thermal_transmittance.measurement_unit.value}, "
            f"Thermal Resistance: {self.thermal_resistance.value} {self.thermal_resistance.measurement_unit.value}"
            f"Solar Heat Gain Coefficient: {self.solar_heat_gain_coefficient}"
        )
