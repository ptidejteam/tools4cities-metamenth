from uuid import uuid4
from typing import List
from subsystem.ventilation_system import VentilationSystem
from typing import Union


class HVACSystem:

    def __init__(self):
        self._UID = str(uuid4())
        self._ventilation_system: List[VentilationSystem] = []

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def ventilation_system(self) -> [VentilationSystem]:
        return self._ventilation_system.copy() if self._ventilation_system else []

    @ventilation_system.setter
    def ventilation_system(self, value: Union[List[VentilationSystem], VentilationSystem]):
        if value is not None:
            if type(value) is list:
                self._ventilation_system.extend(value)
            else:
                self._ventilation_system.append(value)
        else:
            raise ValueError("ventilation_system should be of type VentilationSystem")

    def __str__(self):
        return (
            f"HVACSystem("
            f"UID: {self.UID}, "
            f"Type: {self.ventilation_system})"
        )