"""
Copyright (c) 2023-2025 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

from metamenth.enumerations.abstract_enum import AbstractEnum


class DuctShape(AbstractEnum):
    """
    Shapes of ventilation ducts

    Author: Peter Yefi
    Email: peteryefi@gmail.com
    """
    RECTANGULAR = "Rectangular"
    ROUND = "Round"

