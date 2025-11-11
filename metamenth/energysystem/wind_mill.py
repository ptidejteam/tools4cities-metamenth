"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.energysystem.renewable_energy_system import RenewableEnergySystem
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import WindTurbineType


class WindMill(RenewableEnergySystem):
    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit,
                 number_of_turbine: int, turbine_type: WindTurbineType):
        super().__init__(name, inverter, unit)
        self._number_of_turbines = None
        self._turbine_type = None

        self.number_of_turbines = number_of_turbine
        self.turbine_type = turbine_type

    @property
    def number_of_turbines(self) -> int:
        return self._number_of_turbines

    @number_of_turbines.setter
    def number_of_turbines(self, value: int):
        if value is None:
            raise ValueError("number_of_turbines should be of type int")
        self._number_of_turbines = value

    @property
    def turbine_type(self) -> WindTurbineType:
        return self._turbine_type

    @turbine_type.setter
    def turbine_type(self, value: WindTurbineType):
        if value is None:
            raise ValueError("turbine_type should be of type WindTurbineType")
        self._turbine_type = value

    def __str__(self):
        return (
            f"WindMill("
            f"{super().__str__()}, "
            f"Number of Turbines: {self.number_of_turbines}, "
            f"Turbine Type: {self.turbine_type.value})"
        )
