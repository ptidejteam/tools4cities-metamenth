"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from dataclasses import dataclass
from typing import Dict
from datetime import datetime


@dataclass
class ObservableMessage:
    entity_type: str
    entity_id: str
    state: Dict
    message: str = None
    timestamp = datetime.now()
