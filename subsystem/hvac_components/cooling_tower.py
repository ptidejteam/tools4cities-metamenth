from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent


class CoolingTower(AbstractHVACComponent):
    def __init__(self, name: str):
        """
        Models a cooling tower in an hvac system
        :param name: the unique name of the boiler
        :
        """
        super().__init__(name)

    def __str__(self):
        return (
            f"Cooling Tower ({super().__str__()})"
        )
