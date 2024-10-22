import uuid
from metamenth.enumerations import MeasurementUnit
from metamenth.misc import Validate
from abc import ABC


class AbstractReader(ABC):
    """
    Abstract representation of meters

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, measurement_unit: MeasurementUnit, meter_location: str, manufacturer: str = None):
        """
        Initializes a reader instance.

        :param meter_location: The what3word location of the meter.
        """
        self._UID = str(uuid.uuid4())
        self._meter_location = Validate.validate_what3word(meter_location)
        self._measurement_unit = None
        self._manufacturer = manufacturer

        # apply validation
        self.measurement_unit = measurement_unit

    @property
    def UID(self):
        return self._UID

    @property
    def meter_location(self):
        return self._meter_location

    @meter_location.setter
    def meter_location(self, value):
        self._meter_location = Validate.validate_what3word(value)

    @property
    def measurement_unit(self) -> MeasurementUnit:
        return self._measurement_unit

    @measurement_unit.setter
    def measurement_unit(self, value: MeasurementUnit):
        if value is not None:
            self._measurement_unit = value
        else:
            raise ValueError("measurement_unit must be of type MeasurementUnit")

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value: str):
        self._manufacturer = value

    def get(self, attribute):
        return getattr(self, attribute, None)

    def __eq__(self, other):
        # Meters are equal if they share the same UID
        if isinstance(other, AbstractReader):
            # Check for equality based on the 'UID' attribute
            return self.UID == other.UID and self.measurement_unit == other.measurement_unit
        return False

    def __str__(self):
        """
        :return: A formatted string representing the recorder.
        """

        return (
            f"UID: {self.UID}, "
            f"Measurement Unit: {self.measurement_unit}, "
            f"Manufacturer: {self.manufacturer}"
        )
