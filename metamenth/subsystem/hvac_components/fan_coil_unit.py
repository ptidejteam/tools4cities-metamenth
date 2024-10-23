from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import (
    AbstractDuctConnectedComponent)
from metamenth.subsystem.hvac_components.heat_exchanger import HeatExchanger
from metamenth.subsystem.hvac_components.fan import Fan
from metamenth.enumerations import FCUType
from metamenth.enumerations import FCUPipeSystem


class FanCoilUnit(AbstractDuctConnectedComponent):
    def __init__(self, name: str, heat_exchanger: HeatExchanger,
                 fan: Fan, fcu_type: FCUType, fcu_pipe_system: FCUPipeSystem, is_ducted: bool = True):
        """
        Models a fan coil unit (FCU) in a built environment
        :param name: the unique name of the heat exchanger
        :param heat_exchanger: the heat exchanger which is part of the FCU
        :param fan: the fan which is part of the FCU
        :param fcu_type: the type of FCU
        :param fcu_pipe_system: the piping system of the FCU
        :param is_ducted: indicates if the FCU is connected to ventilation ducts or not
        """
        super().__init__(name)
        self._fan = None
        self._heat_exchanger = None
        self._fcu_type = None
        self._fcu_pipe_system = None
        self._is_ducted = is_ducted

        self.heat_exchanger = heat_exchanger
        self.fan = fan
        self.fcu_type = fcu_type
        self.fcu_pipe_system = fcu_pipe_system

    @property
    def heat_exchanger(self) -> HeatExchanger:
        return self._heat_exchanger

    @heat_exchanger.setter
    def heat_exchanger(self, value: HeatExchanger):
        if value is not None:
            self._heat_exchanger = value
        else:
            raise ValueError("heat_exchanger must be of type HeatExchanger")

    @property
    def fan(self) -> Fan:
        return self._fan

    @fan.setter
    def fan(self, value: Fan):
        if value is not None:
            self._fan = value
        else:
            raise ValueError("fan must be of type Fan")

    @property
    def fcu_type(self) -> FCUType:
        return self._fcu_type

    @fcu_type.setter
    def fcu_type(self, value: FCUType):
        if value is not None:
            self._fcu_type = value
        else:
            raise ValueError("fcu_type must be of type FCUType")

    @property
    def fcu_pipe_system(self) -> FCUPipeSystem:
        return self._fcu_pipe_system

    @fcu_pipe_system.setter
    def fcu_pipe_system(self, value: FCUPipeSystem):
        if value is not None:
            self._fcu_pipe_system = value
        else:
            raise ValueError("fcu_pipe_system must be of type FCUPipeSystem")

    @property
    def is_ducted(self) -> bool:
        return self._is_ducted

    @is_ducted.setter
    def is_ducted(self, value: bool):
        if value is not None:
            self._is_ducted = value
        else:
            raise ValueError("is_ducted must be of type bool")

    def __str__(self):
        return (
            f"FanCoilUnit ({super().__str__()}"
            f"FCU Type: {self.fcu_type}, "
            f"FCU Pipe System: {self.fcu_pipe_system}, "
            f"Is Ducted: {self.is_ducted}, "
            f"Heat Exchanger: {self.heat_exchanger}"
            f"Fan : {self.fan})"
        )
