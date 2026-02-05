"""
Copyright (c) 2023-2026 Peter Yefi.
All rights reserved. This program and the accompanying materials
are made available under the terms of the GNU General Public License v3.0
which accompanies this distribution, and is available at:
https://www.gnu.org/licenses/gpl-3.0.html

Contributors:
    Peter Yefi - API design and implementation
"""

import ifcopenshell
import ifcopenshell.util.element as util_element
import re

class IFC:
    """
    Extract building information from IFC BIM files and outputs them
    as dictionary objects for model instantiation
    """

    def __init__(self, file_path: str):
        """
        :param file_path: The full path to an IFC file
        """
        try:
            self._ifc_bim = ifcopenshell.open(file_path)
            self._ifc_building = None
            # extract building
            buildings = self._ifc_bim.by_type("IfcBuilding")
            if buildings:
                self._ifc_building = buildings[0]
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_building_structure(self):
        return self._get_floors_and_rooms()

    def _get_address(self):
        """
        Converts an IfcPostalAddress into a Python dict
        """
        if hasattr(self._ifc_building, "BuildingAddress"):
            address = self._ifc_building.BuildingAddress
            return {
                "street": list(address.AddressLines)[0] if address.AddressLines else "Unknown Street",
                "city": address.Town or "Unknown City",
                "state": address.Region or "Unknown Region",
                "zip_code": address.PostalCode or "Unknown Zipcode",
                "country": address.Country or "Unknown Country"
            }
        return None

    def _get_building_type(self):


        # First check ObjectType (most common)
        if self._ifc_building.ObjectType:
            return {
                "source": "IfcBuilding.ObjectType",
                "value": self._ifc_building.ObjectType
            }

        # Then check the Property Sets
        psets = util_element.get_psets(self._ifc_building)

        for pset_name, properties in psets.items():
            for key in ["BuildingType", "OccupancyType", "UseType"]:
                if key in properties:
                    return {
                        "source": f"PropertySet::{pset_name}",
                        "value": properties[key]
                    }

        # Then check IfcBuildingType (IFC4)
        for rel in self._ifc_building.IsDefinedBy:
            if rel.is_a("IfcRelDefinesByType"):
                building_type = rel.RelatingType
                if building_type and building_type.Name:
                    return {
                        "source": "IfcBuildingType",
                        "value": building_type.Name
                    }

        return None

    def _get_floors_and_rooms(self):
        result = []

        # Get all storeys (floors)
        storeys = self._ifc_bim.by_type("IfcBuildingStorey")
        elevation_map = self._build_elevation_floor_map(storeys)

        for storey in storeys:
            floor_data = {
                "floor_name": storey.Name,
                "long_name": storey.LongName,
                "elevation": storey.Elevation,
                "floor_number": self._get_floor_number(storey, elevation_map),
                "rooms": []
            }
            # Get elements contained in this storey
            elements = util_element.get_decomposition(storey)

            for element in elements:
                if element.is_a("IfcSpace"):
                    room = {
                        "room_name": element.Name,
                        "long_name": element.LongName,
                        "global_id": element.GlobalId
                    }

                    # Try to extract area (NetFloorArea is common)
                    psets = util_element.get_psets(element)

                    for pset_name, props in psets.items():
                        if "NetFloorArea" in props:
                            room["area"] = props["NetFloorArea"]
                            room["area_source"] = pset_name
                            break

                    floor_data["rooms"].append(room)
            result.append(floor_data)
        return result

    def _parse_floor_number_from_name(self, name: str):
        if not name:
            return None

        name = name.lower()

        # English + French patterns
        patterns = [
            r"level\s*(-?\d+)",
            r"floor\s*(-?\d+)",
            r"étage\s*(-?\d+)",
            r"niveau\s*(-?\d+)",
            r"storey\s*(-?\d+)",
            r"rdc",
            r"rez"
        ]

        for pattern in patterns:
            match = re.search(pattern, name)
            if match:
                if match.groups():
                    return int(match.group(1))
                # RDC / Rez-de-chaussée
                return 0

        return None

    def _get_floor_number(self, storey, elevation_map=None):
        """
        Returns an integer floor number
        """
        # First check Property sets
        psets = util_element.get_psets(storey)
        common = psets.get("Pset_BuildingStoreyCommon", {})

        for key in ["StoreyNumber", "Level", "FloorNumber"]:
            if key in common:
                return int(common[key])

        # Then check the name property
        number_from_name = self._parse_floor_number_from_name(storey.Name)
        if number_from_name is not None:
            return number_from_name

        # 3️⃣ Then check from elevation ordering
        if elevation_map and storey in elevation_map:
            return elevation_map[storey]

        return None

    def _build_elevation_floor_map(self, storeys):
        """
        Maps storeys to floor numbers based on sorted elevation
        """
        sorted_storeys = sorted(
            storeys,
            key=lambda s: s.Elevation if s.Elevation is not None else float("inf")
        )

        return {storey: idx for idx, storey in enumerate(sorted_storeys)}


if __name__ == '__main__':
    ifc_imp = IFC("/Users/peteryefi/yefi/NextGen Cities/Data/Concordia_pilot_rvt_2025.ifc")
    print(ifc_imp.extract_building_structure())
