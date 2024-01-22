from datatypes import BinaryMeasure
from uuid import uuid4
from enumerations import BuildingType
from datatypes import Address
from datatypes import OperationalSchedule
from typing import List
from .floor import Floor
from .envelope import Envelope
from typing import Optional
from measure_instruments import WeatherStation
from measure_instruments import Meter
from visitors import EntityRemover


class Building:
    def __init__(
        self,
        construction_year: int,
        height: BinaryMeasure,
        floorArea: BinaryMeasure,
        internal_mass: BinaryMeasure,
        address: Address,
        building_type: BuildingType,
        floors: List[Floor],
        meters: List[Meter]
    ):
        """
        :param construction_year: The construction year of the building
        :param height: The height of the building
        :param floorArea: The floor area of the building
        :param internal_mass: The internal mass of the building
        :param address: The address of the building
        :param building_type: The type of building
        :param meters: the meter(s) at the building level measure different phenomena
        """
        self.UID = uuid4()
        self.construction_year = construction_year
        self.height = height
        self.floorArea = floorArea
        self.internal_mass = internal_mass
        self.address = address
        self.building_type = building_type
        self.schedules: List[OperationalSchedule] = []
        self.envelope: Envelope = Optional[None]
        self.floors = floors
        self.meters = meters
        self.weather_stations: List[WeatherStation] = []
        if not self.floors:
            raise ValueError("A building must have at least one floor")

    def add_weather_station(self, weather_station: WeatherStation):
        """
        Adds a weather station to a building
        :param weather_station: a station to measure various weather elements
        :return:
        """
        self.weather_stations.append(weather_station)

    def add_meter(self, meter: Meter):
        """
        Adds a meter to a building
        :param meter: a meter to measure some phenomena e.g. energy consumption
        :return:
        """
        self.meters.append(meter)

    def add_schedule(self, schedule: OperationalSchedule):
        """
        Adds an operational schedule to this building
        :param schedule: the schedule
        :return:
        """
        self.schedules.append(schedule)

    def add_envelope(self, envelope: Envelope):
        """
        Adds and envelop to this building
        :param envelope: the building envelop
        :return:
        """
        self.envelope = envelope

    def add_floors(self, floors: List[Floor]):
        """
        Add multiple unique (by floor number) floors to a building
        :param floors: the floors to add to this building
        :return:
        """
        for new_floor in floors:
            existing_floor = next((floor for floor in self.floors if floor.number == new_floor.number), None)
            if existing_floor is None:
                self.floors.append(new_floor)

    def remove_entity(self, visitor: EntityRemover, entity: str, UID: str):
       visitor.remove_building_entity(self, entity, UID)

    def __str__(self):
        floors_info = "\n".join([f"  - Floor {floor.number}: {floor}" for floor in self.floors])
        weather_stations_info = "\n".join([f"  - {station}" for station in self.weather_stations])
        schedules_info = "\n".join([f"  - {schedule}" for schedule in self.schedules])
        meter_info = "\n".join([f"  - {meter}" for meter in self.meters])

        return (f"Layer("
                f"Building UID: {self.UID}, "
                f"Construction Year: {self.construction_year}, "
                f"Height: {self.height}, "
                f"Floor Area: {self.floorArea}, "
                f"Internal Mass: {self.internal_mass}, "
                f"Address: {self.address}, "
                f"Building Type: {self.building_type}, "
                f"Floor Count: {len(self.floors)}, "
                f"Weather Stations Count: {len(self.weather_stations)}, "
                f"Schedules Count: {len(self.schedules)}, "
                f"Floors:\n{floors_info}, "
                f"Weather Stations:\n{weather_stations_info}, "
                f"Schedules:\n{schedules_info}, "
                f"Meters:\n{meter_info}, "
                f"Envelope: {self.envelope}")
