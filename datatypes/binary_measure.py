from enumerations import MeasurementUnit


class BinaryMeasure:
    """
    Represents a binary measure with a value and a measurement unit.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, value: int = 0.0, measurement_unit: MeasurementUnit = None):
        """
        Parameters:
        - value (int): The numerical value of the binary measure.
        - measurement_unit (MeasurementUnit): The measurement unit of the binary measure.
        """
        self.value = value
        self.measurement_unit = measurement_unit

    def __str__(self):
        return f"Value: {self.value}, Measurement Unit: {self.measurement_unit.value}"
