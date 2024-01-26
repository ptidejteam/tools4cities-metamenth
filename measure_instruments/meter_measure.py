from datetime import datetime
import uuid


class MeterMeasure:
    """
    This class represents the reading values of a meter in a building.
    The unit of measurement depends on the phenomenon measured by a meter

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, value: float):
        """
        :param value: The numerical value measured by the meter

        """
        self._UID = uuid.uuid4()
        self._timestamp = datetime.now()
        self._value = None

        # Apply validation
        self.value = value

    @property
    def UID(self):
        return self._UID

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float):
        if value is not None:
            self._value = value
        else:
            raise ValueError("Value must be a float")

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __str__(self):
        """
        :return: A formatted string of the meter readings.
        """
        return (f"MeterMeasure (UID: {self.UID}, Value: {self.value}, "
                f"Timestamp: {self.timestamp})")

