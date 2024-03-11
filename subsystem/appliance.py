from subsystem.interfaces.abstract_subsystem import AbstractSubsystem
from enumerations import ApplianceCategory
from enumerations import ApplianceType
from datatypes.binary_measure import BinaryMeasure
from datatypes.rated_device_measure import RatedDeviceMeasure
from datatypes.continuous_measure import ContinuousMeasure
from transducers.interfaces.abstract_transducer import AbstractTransducer


class Appliance(AbstractSubsystem):
    def __init__(self, name: str, appliance_category: [ApplianceCategory],
                 appliance_type: ApplianceType, manufacturer: str = None,
                 consumption_capacity: BinaryMeasure = None,
                 rated_device_measure: RatedDeviceMeasure = None,
                 operating_conditions: [ContinuousMeasure] = None):
        """
        Defines an appliance in a built environment
        :param name: the unique name of the appliance
        :param appliance_category: the appliance category e.g., home appliance.
        :param appliance_type: the appliance type, e.g., photocopier
        :param manufacturer: the manufacturer of the appliance
        :param consumption_capacity: the power consumption capacity of the appliance
        :param rated_device_measure: the rated device measure of the appliance
        """
        super().__init__(name)
        self._appliance_type = None
        self._manufacturer = manufacturer
        self._consumption_capacity = consumption_capacity
        self._rated_device_measure = rated_device_measure
        self._appliance_category: [ApplianceCategory] = []
        self._operating_conditions: [ContinuousMeasure] = operating_conditions

        self.appliance_type = appliance_type
        self.appliance_category = appliance_category
        self._transducers: [AbstractTransducer] = []

    @property
    def appliance_type(self) -> ApplianceType:
        return self._appliance_type

    @appliance_type.setter
    def appliance_type(self, value: ApplianceType):
        if value is not None:
            self._appliance_type = value
        else:
            raise ValueError("appliance_type must be of type ApplianceType")

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value: str):
        self._manufacturer = value

    @property
    def consumption_capacity(self) -> BinaryMeasure:
        return self._consumption_capacity

    @consumption_capacity.setter
    def consumption_capacity(self, value: BinaryMeasure):
        self._consumption_capacity = value

    @property
    def rated_device_measure(self) -> RatedDeviceMeasure:
        return self._rated_device_measure

    @rated_device_measure.setter
    def rated_device_measure(self, value: RatedDeviceMeasure):
        self._rated_device_measure = value

    @property
    def appliance_category(self) -> [ApplianceCategory]:
        return self._appliance_category.copy()

    @appliance_category.setter
    def appliance_category(self, value: [ApplianceCategory]):
        if value is not None and type(value) is list:
            self._appliance_category.extend(value)
        else:
            raise ValueError("appliance_category should be a list of type ApplianceCategory")

    @property
    def operating_conditions(self) -> [ContinuousMeasure]:
        return self._operating_conditions.copy()

    @operating_conditions.setter
    def operating_conditions(self, value: [ContinuousMeasure]):
        if value is not None and type(value) is list:
            self._operating_conditions.extend(value)

    @property
    def transducers(self) -> [AbstractTransducer]:
        return self._transducers.copy()

    def __str__(self):
        return (
            f"Appliance ({super().__str__()}"
            f"Manufacturer: {self.manufacturer}, "
            f"Appliance Type: {self.appliance_type.value}, "
            f"Appliance Category: {self.appliance_category}, "
            f"Consumption Capacity: {self.consumption_capacity}, "
            f"Operating Conditions: {self.operating_conditions}, "
            f"Rated Device Measure: {self.rated_device_measure})"
        )

