"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.subsystem.interfaces.abstract_ventilation_component import AbstractVentilationComponent
from metamenth.enumerations import RadiantSlabType


class RadiantSlab(AbstractVentilationComponent):

    def __init__(self, name: str, radiate_slab_type: RadiantSlabType):
        super().__init__(name)
        self._radiant_slab_type = None

        self.radiant_slab_type = radiate_slab_type

    @property
    def radiant_slab_type(self) -> RadiantSlabType:
        return self._radiant_slab_type

    @radiant_slab_type.setter
    def radiant_slab_type(self, value: RadiantSlabType):
        if value is not None:
            self._radiant_slab_type = value
        else:
            raise ValueError("radiant_slab_type must be of type RadiantSlabType")

    def __str__(self):
        return (
            f"RadiantSlab ({super().__str__()}"
            f"Type: {self.radiant_slab_type})"
        )

