from subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from enumerations import HeatSource
from subsystem.hvac_components.condenser import Condenser


class HeatPump(AbstractDuctConnectedComponent):
    def __init__(self, name: str, heat_source: HeatSource,  condenser: Condenser = None, manufacturer: str = None):
        """
        Models a heat pump in a built environment
        :param name: the unique name of the heat exchanger
        :param heat_source: the type of heat exchanger
        :param manufacturer: the substance flow type of the heat exchanger
        """
        super().__init__(name)
        self._heat_source = None
        self._manufacturer = manufacturer
        self._condenser = condenser

        self.heat_source = heat_source

    @property
    def heat_source(self) -> HeatSource:
        return self._heat_source

    @heat_source.setter
    def heat_source(self, value: HeatSource):
        if not value:
            raise ValueError("heat_source must be of type HeatSource")
        self._heat_source = value

    @property
    def condenser(self) -> Condenser:
        return self._condenser

    @condenser.setter
    def condenser(self, value: Condenser):
        self._condenser = value

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value: str):
        self._manufacturer = value

    def __str__(self):
        return (
            f"HeatPump ({super().__str__()}"
            f"Heat Source: {self.heat_source.value}, "
            f"Condenser: {self.condenser}, "
            f"Manufacturer : {self.manufacturer})"
        )
