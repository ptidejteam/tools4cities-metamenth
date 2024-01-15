import uuid
from enumerations import MeterType
from enumerations import MeasurementUnit
from measure_instruments import MeterMeasure
from misc import Validate


class Meter:
    """A class representing a meter with specified attributes."""

    def __init__(self, meter_location: str, manufacturer: str, measurement_frequency: float,
                 measurement_unit: MeasurementUnit, meter_type: MeterType):
        """
        Initializes a Meter instance.

        :param meter_location: The what3word location of the meter.
        :param manufacturer: The manufacturer of the meter.
        :param measurement_frequency: The measurement frequency of the meter.
        :param measurement_unit: The measurement unit of the meter data.
        :param meter_type: The type of the meter.
        """
        self.UID = str(uuid.uuid4())
        self.meter_location = Validate.validate_what3word(meter_location)
        self.manufacturer = manufacturer
        self.measurement_frequency = measurement_frequency
        self.measurement_unit = measurement_unit
        self.meter_type = meter_type
        self.meter_measures: [MeterMeasure] = []

    def add_meter_measure(self, value: float):
        """
        Add measurement for this meter
        :param value: The numerical value of the meter measure.
        """
        meter_measure = MeterMeasure(value)
        self.meter_measures.append(meter_measure)

    def __str__(self):
        """
        :return: A formatted string representing the meter.
        """
        meter_details = (f"Meter (UID: {self.UID}, Location: {self.meter_location}, "
                         f"Manufacturer: {self.manufacturer}, Frequency: {self.measurement_frequency}, "
                         f"Unit: {self.measurement_unit.name}, Type: {self.meter_type.name})")

        measurements = "\n".join(str(measure) for measure in self.meter_measures)

        return f"{meter_details}\nMeasurements:\n{measurements}"
