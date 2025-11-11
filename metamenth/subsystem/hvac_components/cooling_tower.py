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
