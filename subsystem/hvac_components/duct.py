from uuid import uuid4
from enumerations import DuctType
from datatypes.interfaces.abstract_dynamic_entity import AbstractDynamicEntity
from datatypes.interfaces.abstract_zonal_entity import AbstractZonalEntity


class Duct(AbstractDynamicEntity, AbstractZonalEntity):

    def __init__(self, name: str, duct_type: DuctType):
        AbstractDynamicEntity.__init__(self)
        AbstractZonalEntity.__init__(self)
        self._UID = str(uuid4())
        self._name = None
        self._duct_type = None
        self._duct_sub_type = None
        self._connections = None

        self.name = name
        self.duct_type = duct_type
