from metamenth.energysystem.renewable_energy_system import RenewableEnergySystem
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import SolarPVType
from metamenth.enumerations import CellType
from metamenth.datatypes.binary_measure import BinaryMeasure


class SolarPV(RenewableEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit,
                 solar_pv_type: SolarPVType, cell_type: CellType):
        super().__init__(name, inverter, unit)
        self._solar_pv_type = None
        self._cell_type = None
        self._thermal_capacity = None
        self._module_area = None

        self.cell_type = cell_type
        self.solar_pv_type = solar_pv_type

    @property
    def solar_pv_type(self) -> SolarPVType:
        return self._solar_pv_type

    @solar_pv_type.setter
    def solar_pv_type(self, value: SolarPVType):
        if value is None:
            raise ValueError("solar_pv_type should be of type SolarPVType")
        self._solar_pv_type = value

    @property
    def cell_type(self) -> CellType:
        return self._cell_type

    @cell_type.setter
    def cell_type(self, value: CellType):
        if value is None:
            raise ValueError("cell_type should be of type CellType")
        self._cell_type = value

    @property
    def thermal_capacity(self) -> BinaryMeasure:
        return self._thermal_capacity

    @thermal_capacity.setter
    def thermal_capacity(self, value: BinaryMeasure):
        self._thermal_capacity = value

    @property
    def module_area(self) -> BinaryMeasure:
        return self._module_area

    @module_area.setter
    def module_area(self, value: BinaryMeasure):
        self._module_area = value

    def __str__(self):
        return (
            f"SolarPV("
            f"{super().__str__()}, "
            f"Solar PV Type: {self.solar_pv_type.value}, "
            f"Cell Type: {self.cell_type.value}, "
            f"Thermal Capacity: {self.thermal_capacity}, "
            f"Module Area: {self.module_area})"
        )
