from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from enumerations import DamperType


class Damper(AbstractHVACComponent):
    def __init__(self, name: str, damper_type: DamperType, percentage_opened: float = 0.0):
        """
        Models a damper in an hvac system
        :param name: the unique name of the heat exchanger
        :param damper_type: the type of damper
        :param percentage_opened: how wide the damper is opened
        """
        super().__init__(name)
        self._damper_type = None
        self._percentage_opened = percentage_opened

        self.damper_type = damper_type

    @property
    def damper_type(self) -> DamperType:
        return self._damper_type

    @damper_type.setter
    def damper_type(self, value: DamperType):
        if value is not None:
            self._damper_type = value
        else:
            raise ValueError("damper_type must be of type DamperType")

    @property
    def percentage_opened(self) -> float:
        return self._percentage_opened

    @percentage_opened.setter
    def percentage_opened(self, value: float):
        self._percentage_opened = value

    def __str__(self):
        return (
            f"Damper ({super().__str__()}"
            f"Type: {self.damper_type}, "
            f"Percentage Opened : {self.percentage_opened})"
        )
