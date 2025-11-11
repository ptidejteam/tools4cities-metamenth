"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from metamenth.enumerations import CompressorType


class Compressor(AbstractDuctConnectedComponent):
    def __init__(self, name: str, compressor_type: CompressorType):
        """
        Models a compressor in hvac system
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
