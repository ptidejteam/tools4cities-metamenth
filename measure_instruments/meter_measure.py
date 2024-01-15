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
        self.UID = uuid.uuid4()  # Automatically generated unique identifier
        self.timestamp = datetime.now()
        self.value = value

    def __str__(self):
        """
        :return: A formatted string of the meter readings.
        """
        return (f"MeterMeasure (UID: {self.UID}, Value: {self.value}, "
                f"Timestamp: {self.timestamp})")

