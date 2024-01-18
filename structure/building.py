from datatypes import BinaryMeasure
from uuid import uuid4
from enumerations import BuildingType
from datatypes import Address
from datatypes import OperationalSchedule
from typing import List
from .floor import Floor
from .envelope import Envelope
from typing import Optional


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
    ):
        """
        :param construction_year: The construction year of the building
        :param height: The height of the building
        :param floorArea: The floor area of the building
        :param internal_mass: The internal mass of the building
        :param address: The address of the building
        :param building_type: The type of building
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
        if not self.floors:
            raise ValueError("A building must have at least one floor")

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
