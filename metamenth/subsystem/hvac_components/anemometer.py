from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.enumerations import AnemometerType


class Anemometer(AbstractHVACComponent):
    def __init__(self, name: str, anemometer_type: AnemometerType):
        """
        Models a damper in hvac system
        :param name: the unique name of the heat exchanger
        :param anemometer_type: the type of anemometer
        """
        super().__init__(name)
        self._anemometer_type = None
        self.anemometer_type = anemometer_type

    @property
    def anemometer_type(self) -> AnemometerType:
        return self._anemometer_type

    @anemometer_type.setter
    def anemometer_type(self, value: AnemometerType):
        if value is not None:
            self._anemometer_type = value
        else:
            raise ValueError("anemometer_type must be of type AnemometerType")

    def __str__(self):
        return (
            f"Anemometer ({super().__str__()}"
            f"Type: {self.anemometer_type})"
        )
