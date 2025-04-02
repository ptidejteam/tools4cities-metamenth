"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.observers.interfaces.observer import Observer
from metamenth.datatypes.observable_message import ObservableMessage
from dataclasses import asdict


class StructureStateChangeLogger(Observer):
    """
    State logger for structure entities
    """

    def __init__(self):
        self._state_log: [ObservableMessage] = []

    def log_state(self, message: ObservableMessage):
        self._state_log.append(asdict(message))

    @property
    def state_log(self):
        return self._state_log
