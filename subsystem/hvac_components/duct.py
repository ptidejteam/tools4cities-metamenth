from uuid import uuid4
from enumerations import DuctType
from datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity
from datatypes.interfaces.abstract_zonal_entity import AbstractZonalEntity
from subsystem.hvac_components.damper import Damper
from subsystem.hvac_components.fan import Fan
from subsystem.hvac_components.heat_exchanger import HeatExchanger
from typing import List


class Duct(AbstractDynamicEntity, AbstractZonalEntity):

    def __init__(self, name: str, duct_type: DuctType):
        AbstractDynamicEntity.__init__(self)
        AbstractZonalEntity.__init__(self)
        self._UID = str(uuid4())
        self._name = None
        self._duct_type = None
        self._duct_sub_type = None
        self._connections = None
        self._heat_exchangers: List[HeatExchanger] = []
        self._fans: List[Fan] = []
        self._dampers: List[Damper] = []

        self.name = name
        self.duct_type = duct_type
