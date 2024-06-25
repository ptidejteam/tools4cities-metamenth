from energysystem.interfaces.abstract_electrical import AbstractElectrical
from enumerations import PowerState


class AutomaticTransferSwitch(AbstractElectrical):
    def __init__(self, name: str, power_state: PowerState):
        super().__init__(name, power_state)
        self._power_source_type = None
        self._transition_type = None
        self._operation_mode = None
        self._switching_mechanism = None

    @property
    def power_source_type(self):
        return self._power_source_type

    @power_source_type.setter
    def power_source_type(self, value):
        self._power_source_type = value

    @property
    def transition_type(self):
        return self._transition_type

    @transition_type.setter
    def transition_type(self, value):
        self._transition_type = value

    @property
    def operation_mode(self):
        return self._operation_mode

    @operation_mode.setter
    def operation_mode(self, value):
        self._operation_mode = value

    @property
    def switching_mechanism(self):
        return self._switching_mechanism

    @switching_mechanism.setter
    def switching_mechanism(self, value):
        self._switching_mechanism = value

    def __str__(self):
        return (
            f"AutomaticTransferSwitch("
            f"{super().__str__()}"
            f"Power Source Type: {self.power_source_type}, "
            f"Transition Type: {self.transition_type}, "
            f"Operation Mode: {self.operation_mode}, "
            f"Switching Mechanism: {self.switching_mechanism})"
        )

