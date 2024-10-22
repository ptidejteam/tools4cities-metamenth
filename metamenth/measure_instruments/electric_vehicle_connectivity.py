from metamenth.measure_instruments.interfaces.abstract_data_measure import AbstractDataMeasure
from metamenth.enumerations import OperationType
from metamenth.misc import Validate


class ElectricVehicleConnectivity(AbstractDataMeasure):
    """
    This class represents the reading values of EV charging meter.
    The unit of measurement depends on the phenomenon measured by a meter

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, value: float, start_time: str, end_time: str, operation_type: OperationType, vehicle_id: str):
        """
        :param value: The numerical value measured
        :param start_time: the start timestamp for charging/discharging
        :param end_time: the end timestamp of charging/discharging
        :param operation_type: either charging or discharging
        :param vehicle_id: the id of the vehicle to charged or discharged

        """
        super().__init__(value, start_time)
        self._end_time = None
        self._operation_type = None
        self._vehicle_uid = None

        self.end_time = end_time
        self.operation_type = operation_type
        self.vehicle_uid = vehicle_id

    @property
    def end_time(self) -> str:
        return self._end_time

    @end_time.setter
    def end_time(self, value: str):
        if value is None:
            raise ValueError('end_time must be of type str')
        self._end_time = Validate.parse_date(value)

    @property
    def operation_type(self) -> OperationType:
        return self._operation_type

    @operation_type.setter
    def operation_type(self, value: OperationType):
        if value is None:
            raise ValueError('operation_type must be of type OperationType')
        self._operation_type = value

    @property
    def vehicle_uid(self) -> str:
        return self._vehicle_uid

    @vehicle_uid.setter
    def vehicle_uid(self, value: str):
        if value is None:
            raise ValueError('vehicle_uid must be of type str')
        self._vehicle_uid = value

