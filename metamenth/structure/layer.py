"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

import uuid
from metamenth.datatypes.interfaces.abstract_measure import AbstractMeasure
from metamenth.structure.material import Material
from metamenth.enumerations import LayerRoughness


class Layer:
    """
    A layer in the envelope of a building

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    def __init__(
        self,
        height: AbstractMeasure,
        length: AbstractMeasure,
        thickness: AbstractMeasure,
        material: Material,
        roughness: LayerRoughness = None,
        has_vapour_barrier: bool = False,
        has_air_barrier: bool = False,

    ):
        self._UID = str(uuid.uuid4())  # Generate a unique identifier
        self._height = None
        self._length = None
        self._thickness = None
        self._material = None
        self._roughness = None
        self._has_vapour_barrier = has_vapour_barrier
        self._has_air_barrier = has_air_barrier
        self._order = 1 # where the layer is located in a block. 1 is the innermost layer

        # apply validation with setters
        self.height = height
        self.length = length
        self.thickness = thickness
        self.material = material
        self.roughness = roughness

    @property
    def UID(self) -> str:
        return self._UID

    @property
    def height(self) -> AbstractMeasure:
        return self._height

    @height.setter
    def height(self, value: AbstractMeasure):
        if value is None:
            raise ValueError("height should be of type BinaryMeasure")
        self._height = value

    @property
    def length(self) -> AbstractMeasure:
        return self._length

    @length.setter
    def length(self, value: AbstractMeasure):
        if value is None:
            raise ValueError("length should be of type BinaryMeasure")
        self._length = value

    @property
    def thickness(self) -> AbstractMeasure:
        return self._thickness

    @thickness.setter
    def thickness(self, value: AbstractMeasure):
        if value is None:
            raise ValueError("thickness should be of type BinaryMeasure")
        self._thickness = value

    @property
    def material(self) -> Material:
        return self._material

    @material.setter
    def material(self, value: Material):
        if value is None:
            raise ValueError("material cannot be None")
        self._material = value

    @property
    def roughness(self) -> LayerRoughness:
        return self._roughness

    @roughness.setter
    def roughness(self, value: LayerRoughness):
        self._roughness = value

    @property
    def has_vapour_barrier(self) -> bool:
        return self._has_vapour_barrier

    @has_vapour_barrier.setter
    def has_vapour_barrier(self, value: bool):
        self._has_vapour_barrier = value

    @property
    def has_air_barrier(self) -> bool:
        return self._has_air_barrier

    @has_air_barrier.setter
    def has_air_barrier(self, value: bool):
        self._has_air_barrier = value

    @property
    def order(self) -> int:
        return self._order

    @order.setter
    def order(self, value: int):
        if value is None or value < 1:
            raise ValueError("order should be of type int starting from 1")
        self._order = value

    def __str__(self):
        material_str = f"Material: {str(self.material)}" if self.material else "Material: None"
        return (
            f"Layer("
            f"UID: {self.UID}, "
            f"Height: {self.height.value} {self.height.measurement_unit}, "
            f"Length: {self.length.value} {self.length.measurement_unit}, "
            f"Thickness: {self.thickness.value} {self.thickness.measurement_unit}, "
            f"Roughness: {self.roughness.value if self.roughness else ''}, "
            f"Vapour Barrier: {self.has_vapour_barrier}, "
            f"Air Barrier: {self.has_air_barrier}, "
            f"Order: {self.order}, "
            f"{material_str})"
        )
