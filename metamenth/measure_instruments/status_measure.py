from metamenth.measure_instruments.interfaces.abstract_data_measure import AbstractDataMeasure


class StatusMeasure(AbstractDataMeasure):

    def __init__(self, status: str, timestamp: str = None):
        """
        :param status: The string value measured
        :param timestamp: the time of measurement
        """
        super().__init__(status, timestamp)

