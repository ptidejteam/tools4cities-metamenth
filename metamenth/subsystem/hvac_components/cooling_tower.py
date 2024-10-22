from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent


class CoolingTower(AbstractDuctConnectedComponent):
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
