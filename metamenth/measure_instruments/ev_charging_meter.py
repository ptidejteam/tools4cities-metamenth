from metamenth.enumerations import MeasurementUnit
from metamenth.measure_instruments.interfaces.abstract_reader import AbstractReader
from metamenth.measure_instruments.electric_vehicle_connectivity import ElectricVehicleConnectivity
from metamenth.utils import EntityInsert
from metamenth.utils import StructureEntitySearch
from typing import Dict
from metamenth.enumerations import BuildingEntity


class EVChargingMeter(AbstractReader):
    """
    A representation of an electric vehicle charging meter

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """

    def __init__(self, meter_location: str, measurement_unit: MeasurementUnit,
                 manufacturer: str = None):
        """
        Initializes a Meter instance.

        :param meter_location: The what3word location of the meter.
        :param manufacturer: The manufacturer of the meter.
        :param measurement_unit: The measurement unit of the meter data.
        """
        super().__init__(measurement_unit, meter_location, manufacturer)
        self._vehicle_connectivity: [ElectricVehicleConnectivity] = []

    def get_connectivity_data(self, search_terms: Dict = None) -> [ElectricVehicleConnectivity]:
        """
        Search meter recordings by attributes values
        :param search_terms: a dictionary of attributes and their values
        :return [ElectricVehicleConnectivity]:
        """
        return StructureEntitySearch.search(self._vehicle_connectivity, search_terms)

    def get_connectivity_data_by_date(self, from_timestamp: str, to_timestamp: str = None) -> [ElectricVehicleConnectivity]:
        """
        searches meter recordings based on provided timestamp
        :param from_timestamp: the start timestamp
        :param to_timestamp: the end timestamp
        :return: [ElectricVehicleConnectivity]
        """
        return StructureEntitySearch.date_range_search(self._vehicle_connectivity, from_timestamp, to_timestamp)

    def add_meter_measure(self, connectivity_data: ElectricVehicleConnectivity):
        """
        Add vehicle connectivity for this meter
        :param connectivity_data: the recorded electric vehicle charging or discharging by the meter.
        """
        EntityInsert.insert_building_entity(self._vehicle_connectivity, connectivity_data, BuildingEntity.SCHEDULE.value)

    def __str__(self):
        """
        :return: A formatted string representing the meter.
        """

        return (
            f"EVChargingMeter("
            f"{super().__str__()})"
        )
