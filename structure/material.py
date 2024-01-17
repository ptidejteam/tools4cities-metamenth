from enumerations import MaterialType
from datatypes import BinaryMeasure
import uuid


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
        density: BinaryMeasure,
        heat_capacity: BinaryMeasure,
        thermal_transmittance: BinaryMeasure,
        thermal_resistance: BinaryMeasure,
    ):
        self.UID = str(uuid.uuid4())
        self.description = description
        self.material_type = material_type
        self.density = density
        self.heat_capacity = heat_capacity
        self.thermal_transmittance = thermal_transmittance
        self.thermal_resistance = thermal_resistance

    def __str__(self):
        return (
            f"Material("
            f"UID: {self.UID}, "
            f"Description: {self.description}, "
            f"Type: {self.material_type}, "
            f"Density: {self.density.value} {self.density.measurement_unit}, "
            f"Heat Capacity: {self.heat_capacity.value} {self.heat_capacity.measurement_unit}, "
            f"Thermal Transmittance: {self.thermal_transmittance.value} {self.thermal_transmittance.measurement_unit}, "
            f"Thermal Resistance: {self.thermal_resistance.value} {self.thermal_resistance.measurement_unit})"
        )
