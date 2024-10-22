import uuid
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.misc import Validate
from metamenth.virtual.interfaces.abstract_zonal_entity import AbstractZonalEntity
from metamenth.datatypes.schedulable_entity import SchedulableEntity
from metamenth.structure.envelope import Envelope


class AbstractSpace(AbstractZonalEntity):
    """
    An abstract class for spaces in a building
    """

    def __init__(self, area: AbstractMeasure, location: str = None):
        """
        :param area: The area of the space.
        :param location: The location of the space (three words delimited with two periods).
        """
        super().__init__()
        self._UID = str(uuid.uuid4())
        self._area = None
        self._location = None
        self._schedulable_entity = SchedulableEntity()
        self._envelope = None

        # Apply validation
        self.area = area
        self.location = location

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def area(self) -> AbstractMeasure:
        return self._area

    @area.setter
    def area(self, value: AbstractMeasure):
        if value is None:
            raise ValueError('area must be of type BinaryMeasure')
        self._area = value

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, value: str):
        self._location = Validate.validate_what3word(value)

    @property
    def schedulable_entity(self) -> SchedulableEntity:
        return self._schedulable_entity

    @schedulable_entity.setter
    def schedulable_entity(self, value: SchedulableEntity):
        if value is None:
            raise ValueError("schedules should be of type SchedulableEntity")
        self._schedulable_entity = value

    @property
    def envelope(self) -> Envelope:
        return self._envelope

    @envelope.setter
    def envelope(self, value: Envelope):
        self._envelope = value

    def accept(self, visitor):
        pass

    def get(self, attribute):
        return getattr(self, attribute, None)

    def __str__(self):
        return (
            f"UID: {self.UID}, "
            f"Area: {self.area}, "
            f"Location: {self.location}, "
            f"Zones: {self._zones}, "
            f"Envelope: {self._envelope}, "
            f"Operational Schedule: {self._schedulable_entity}, "
        )
