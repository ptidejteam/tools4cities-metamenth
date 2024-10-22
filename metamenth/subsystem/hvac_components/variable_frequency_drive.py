from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.enumerations import MeasurementUnit


class VariableFrequencyDrive(AbstractHVACComponent):
    def __init__(self, name: str, motor_speed: float = 0.0, max_motor_speed: float = 1000.0,
                 speed_measure: MeasurementUnit = MeasurementUnit.REVOLUTIONS_PER_MINUTE):
        """
        Models a boiler in an hvac system
        :param name: the unique name of the boiler
        :param motor_speed: the speed of the VFD
        :param max_motor_speed: the maximum motor speed of the VFD
        :param speed_measure: the measure unit for the motor speed
        :
        """
        super().__init__(name)
        self._motor_speed = motor_speed
        self._max_motor_speed = max_motor_speed
        self._speed_measure = speed_measure

    @property
    def motor_speed(self) -> float:
        return self._motor_speed

    @property
    def max_motor_speed(self) -> float:
        return self._max_motor_speed

    @property
    def speed_measure(self) -> MeasurementUnit:
        return self._speed_measure

    @motor_speed.setter
    def motor_speed(self, value: float):
        if 0 < value <= self._max_motor_speed:
            self._motor_speed = value
        else:
            raise ValueError("motor_speed must be a number greater than 0 and lesser than the maximum motor speed")

    @max_motor_speed.setter
    def max_motor_speed(self, value: float):
        if 0 < value >= self._motor_speed:
            self._max_motor_speed = value
        else:
            raise ValueError("max_motor_speed must be a number greater than 0 and greater than or equal motor speed")

    @speed_measure.setter
    def speed_measure(self, value: MeasurementUnit):
        if value is not None:
            self._speed_measure = value
        else:
            raise ValueError("speed_measure must be of type MeasurementUnit")

    def __str__(self):
        return (
            f"Variable Frequency Drive ({super().__str__()}"
            f"Motor Speed: {self.motor_speed}, "
            f"Maximum Motor Speed: {self._max_motor_speed}, "
            f"Speed Measure: {self.speed_measure})"
        )
