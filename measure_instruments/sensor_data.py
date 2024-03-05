from measure_instruments.interfaces.abstract_data_measure import AbstractDataMeasure


class SensorData(AbstractDataMeasure):

    def __init__(self, value: float, timestamp: str = None):
        super().__init__(value, timestamp)

