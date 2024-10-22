from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from metamenth.enumerations import HeatExchangerType
from metamenth.enumerations import HeatExchangerFlowType


class HeatExchanger(AbstractDuctConnectedComponent):
    def __init__(self, name: str, heat_exchanger_type: HeatExchangerType,
                 heat_exchanger_flow_type: HeatExchangerFlowType):
        """
        Models a heat exchanger in a built environment
        :param name: the unique name of the heat exchanger
        :param heat_exchanger_type: the type of heat exchanger
        :param heat_exchanger_flow_type: the substance flow type of the heat exchanger
        """
        super().__init__(name)
        self._heat_exchanger_type = None
        self._heat_exchanger_flow_type = None

        self.heat_exchanger_type = heat_exchanger_type
        self.heat_exchanger_flow_type = heat_exchanger_flow_type

    @property
    def heat_exchanger_type(self) -> HeatExchangerType:
        return self._heat_exchanger_type

    @heat_exchanger_type.setter
    def heat_exchanger_type(self, value: HeatExchangerType):
        if value is not None:
            self._heat_exchanger_type = value
        else:
            raise ValueError("heat_exchanger_type must be of type HeatExchangerType")

    @property
    def heat_exchanger_flow_type(self) -> HeatExchangerFlowType:
        return self._heat_exchanger_flow_type

    @heat_exchanger_flow_type.setter
    def heat_exchanger_flow_type(self, value: HeatExchangerFlowType):
        if value is not None:
            self._heat_exchanger_flow_type = value
        else:
            raise ValueError("heat_exchanger_flow_type must be of type HeatExchangerFlowType")

    def __str__(self):
        return (
            f"HeatExchanger ({super().__str__()}"
            f"Type: {self.heat_exchanger_type.value}, "
            f"Flow Type : {self.heat_exchanger_flow_type.value})"
        )
