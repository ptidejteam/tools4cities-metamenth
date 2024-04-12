from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent


class AbstractDuctConnectedComponent(AbstractHVACComponent):

    def __init__(self, name: str):
        super().__init__(name)

        self._ducts: [] = []

    @property
    def ducts(self) -> []:
        return self._ducts.copy()

    def add_duct(self, duct):
        from subsystem.hvac_components.duct import Duct
        if duct is not None and isinstance(duct, Duct):
            self._ducts.append(duct)
        else:
            raise ValueError("value provided is not a duct")

    def __str__(self):
        return (
            f"({super().__str__()}"
            f"Ducts {self.ducts}, "
        )