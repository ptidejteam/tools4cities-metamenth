from uuid import uuid4
from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from typing import List


class HVACSystem:

    def __init__(self):
        self._UID = str(uuid4())
        # TODO: components include engine in energy systems
        self._components: List[AbstractHVACComponent]
        self._ducts: []