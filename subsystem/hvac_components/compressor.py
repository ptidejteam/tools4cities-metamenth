from subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from enumerations import CompressorType


class Compressor(AbstractHVACComponent):
    def __init__(self, name: str, compressor_type: CompressorType):
        """
        Models a compressor in an hvac system
        :param name: the unique name of the compressor
        :param compressor_type: the type of compressor
        """
        super().__init__(name)
        self._compressor_type = None

        self.compressor_type = compressor_type

    @property
    def compressor_type(self) -> CompressorType:
        return self._compressor_type

    @compressor_type.setter
    def compressor_type(self, value: CompressorType):
        if value is not None:
            self._compressor_type = value
        else:
            raise ValueError("compressor_type must be of type CompressorType")

    def __str__(self):
        return (
            f"Compressor ({super().__str__()}"
            f"Type: {self.compressor_type})"
        )
