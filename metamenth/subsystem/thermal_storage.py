from metamenth.subsystem.interfaces.abstract_ventilation_component import AbstractVentilationComponent


class ThermalStorage(AbstractVentilationComponent):

    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return (
            f"ThermalStorage ({super().__str__()})"
        )

