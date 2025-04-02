"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.datatypes.relationships.interfaces.abstract_relationship import AbstractRelationship
from metamenth.enumerations import RelationshipName
from metamenth.subsystem.hvac_components.interfaces.abstract_hvac_component import AbstractHVACComponent
from metamenth.subsystem.hvac_components.interfaces.abstract_duct_connected_component import AbstractDuctConnectedComponent
from typing import Union
from typing import List


class OneToMany(AbstractRelationship):

    def __init__(self, name: RelationshipName, hvac_component: Union[List[AbstractHVACComponent],
    List[AbstractDuctConnectedComponent]]):
        super().__init__(name)
        self.component = hvac_component
