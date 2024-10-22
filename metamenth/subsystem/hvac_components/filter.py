from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.enumerations import FilterType
from metamenth.datatypes.binary_measure import BinaryMeasure
from metamenth.misc import Validate


class Filter(AbstractHVACComponent):
    def __init__(self, name: str, filter_type: FilterType, air_flow_rate: BinaryMeasure = None,
                 life_span: int = None, efficiency: int = None):
        """
        Models a filter in hvac systems
        :param name: the unique name of the heat exchanger
        :param filter_type: the type of filter
        :param air_flow_rate: the rate of air flow usually measured in cubic feet per meter
        :param life_span: the life span in days, of the filter
        :param efficiency: a number from 1 to 16 indicating how efficient the filter is
        """
        super().__init__(name)
        self._filter_type = None
        self._air_flow_rate = air_flow_rate
        self._life_span = None
        self._efficiency = None

        self.filter_type = filter_type
        self.life_span = life_span
        self.efficiency = efficiency

    @property
    def filter_type(self) -> FilterType:
        return self._filter_type

    @filter_type.setter
    def filter_type(self, value: FilterType):
        if value is not None:
            self._filter_type = value
        else:
            raise ValueError("filter_type must be of type FilterType")

    @property
    def air_flow_rate(self) -> BinaryMeasure:
        return self._air_flow_rate

    @air_flow_rate.setter
    def air_flow_rate(self, value: BinaryMeasure):
        self._air_flow_rate = value

    @property
    def life_span(self) -> int:
        return self._life_span

    @life_span.setter
    def life_span(self, value: int):
        if value:
            if value > 0:
                self._life_span = value
            else:
                raise ValueError('life_span must be a positive integer')

    @property
    def efficiency(self) -> int:
        return self._efficiency

    @efficiency.setter
    def efficiency(self, value: int):
        self._efficiency = Validate.validate_number_range(value, (1, 16))

    def __str__(self):
        return (
            f"Filter ({super().__str__()}"
            f"Filter Type: {self.filter_type}, "
            f"Lifespan: {self.life_span}, "
            f"Air Flow Rate: {self.air_flow_rate}, "
            f"Efficiency: {self.efficiency})"
        )
