from measure_instruments.interface.abstract_data_measure import AbstractDataMeasure


class SensorData(AbstractDataMeasure):

    def __init__(self, value: float):
        super().__init__(value)

