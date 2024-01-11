from enumerations import MeasurementUnit


class BinaryMeasure:
    """
    Represents a binary measure with a value and a measurement unit.

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, value: int, measurement_unit: MeasurementUnit):
        """
        Parameters:
        - value (int): The numerical value of the binary measure.
        - measurement_unit (MeasurementUnit): The measurement unit of the binary measure.
        """
        self.value = value
        self.measurement_unit = measurement_unit

    def __str__(self):
        """
        Returns a string representation of BinaryMeasure.

        Returns:
        str: A string representing the value and measurement unit.
        """
        return f"Value: {self.value}, Measurement Unit: {self.measurement_unit.value}"
