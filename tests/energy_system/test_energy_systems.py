from unittest import TestCase
from energysystem.engine import Engine
from enumerations import MeasurementUnit
from enumerations import EngineType
from enumerations import EngineSubType
from enumerations import EngineMode


class TestEnergySystems(TestCase):

    def setUp(self) -> None:
        pass

    def test_engine_without_type(self):
        try:
            _ = Engine("Gen Engine", True, MeasurementUnit.KILOWATTS_PER_HOUR,
                        None, EngineSubType.DIESEL, EngineMode.FUEL)
        except ValueError as err:
            self.assertEqual(err.__str__(), "engine_type should be of type EngineType")

    def test_fuel_cell_engine(self):
        engine = Engine("Gen Engine", True, MeasurementUnit.KILOWATTS_PER_HOUR,
                        EngineType.FUEL_CELL, EngineSubType.HYDROGEN, EngineMode.FUEL)
