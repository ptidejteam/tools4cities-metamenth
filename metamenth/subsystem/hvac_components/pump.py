from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from metamenth.enumerations import PumpType
from metamenth.datatypes.binary_measure import BinaryMeasure
from metamenth.misc.validate import Validate


class Pump(AbstractDuctConnectedComponent):
    def __init__(self, name: str, pump_type: PumpType,
                 flow_rate: BinaryMeasure = None,
                 power_consumption: BinaryMeasure = None,
                 efficiency: float = None):
        """
        Models a pump in a built environment
        :param name: the unique name of pump
        :param pump_type: the type of pump
        :param flow_rate: the flow rate of the pump mostly measured in liters per second (L/s)
        :param power_consumption: the power consumption of the pump in kilowatts (kW)
        :param efficiency: the efficiency of the pump (as a percentage, between 0 and 100)
        """
        super().__init__(name)
        self._pump_type = None
        self._power_consumption = power_consumption
        self._flow_rate = None
        self._efficiency = None

        self.flow_rate = flow_rate
        self.efficiency = efficiency
        self.pump_type = pump_type

    @property
    def pump_type(self) -> PumpType:
        return self._pump_type

    @pump_type.setter
    def pump_type(self, value: PumpType):
        if value is not None:
            self._pump_type = value
        else:
            raise ValueError("heat_exchanger_type must be of type HeatExchangerType")

    @property
    def power_consumption(self) -> BinaryMeasure:
        return self._power_consumption

    @power_consumption.setter
    def power_consumption(self, value: BinaryMeasure):
        self._power_consumption = value

    @property
    def flow_rate(self) -> BinaryMeasure:
        return self._flow_rate

    @flow_rate.setter
    def flow_rate(self, data: BinaryMeasure):
        if data and data.value > 0:
            self._flow_rate = data

    @property
    def efficiency(self) -> float:
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value: float):
        self._efficiency = Validate.validate_number_range(value, (0, 1))


    def __str__(self):
        return (
            f"Pump ({super().__str__()}"
            f"Type: {self.pump_type.value}, "
            f"Flow Rate : {self.flow_rate.value if self.flow_rate else None}, "
            f"{self.flow_rate.measurement_unit if self.flow_rate else None}, "
            f"Efficiency: {self.efficiency}, "
            f"Power Consumption: {self.power_consumption.value if self.power_consumption else None}, "
            f"{self.power_consumption.measurement_unit if self.power_consumption else None})"
        )
