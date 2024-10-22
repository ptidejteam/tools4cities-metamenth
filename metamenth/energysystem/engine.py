from metamenth.energysystem.non_renewable_energy_system import NonRenewableEnergySystem
from metamenth.enumerations import MeasurementUnit
from metamenth.enumerations import EngineType
from metamenth.enumerations import EngineMode
from metamenth.enumerations import EngineSubType
from metamenth.misc import Validate


class Engine(NonRenewableEnergySystem):

    def __init__(self, name: str, inverter: bool, unit: MeasurementUnit,
                 engine_type: EngineType, engine_sub_type: EngineSubType, engine_mode: EngineMode):
        super().__init__(name, inverter, unit)
        self._engine_type = None
        self._engine_mode = None
        self._engine_sub_type = None

        self.engine_type = engine_type
        self.engine_mode = engine_mode
        self.engine_sub_type = engine_sub_type

    @property
    def engine_type(self) -> EngineType:
        return self._engine_type

    @engine_type.setter
    def engine_type(self, value: EngineType):
        if value is None:
            raise ValueError("engine_type should be of type EngineType")
        self._engine_type = value

    @property
    def engine_sub_type(self) -> EngineSubType:
        return self._engine_sub_type

    @engine_sub_type.setter
    def engine_sub_type(self, value: EngineSubType):
        if value is None:
            raise ValueError("engine_sub_type should be of type EngineSubType")
        else:
            if Validate.validate_engine_fuel(self.engine_type.value, value.value):
                self._engine_sub_type = value
            else:
                raise ValueError(f'{value} is an invalid value for {self.engine_type}')

    @property
    def engine_mode(self) -> EngineMode:
        return self._engine_mode

    @engine_mode.setter
    def engine_mode(self, value: EngineMode):
        if value is None:
            raise ValueError("engine_mode should be of type EngineMode")
        self._engine_mode = value

    def __str__(self):
        return (
            f"Engine("
            f"{super().__str__()}, "
            f"Engine Type: {self.engine_type.value}, "
            f"Engine SubType: {self.engine_sub_type.value}, "
            f"Engine Mode: {self.engine_mode.value})"
        )
