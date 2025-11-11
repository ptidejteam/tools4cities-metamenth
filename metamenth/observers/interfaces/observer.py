"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from abc import ABC
from abc import abstractmethod
from metamenth.datatypes.observable_message import ObservableMessage


# Observer interface
class Observer(ABC):
    """
    An interface that defines method to log state of entities
    that need their state to be tracked
    """
    @abstractmethod
    def log_state(self, message: ObservableMessage):
        """
        logs the state of an object
        :param message: object {entity_type, entity_id, state, message}
        :return:
        """
        pass
