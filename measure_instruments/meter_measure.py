from measure_instruments.interface.abstract_data_measure import AbstractDataMeasure


class MeterMeasure(AbstractDataMeasure):
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
        super().__init__(value)
