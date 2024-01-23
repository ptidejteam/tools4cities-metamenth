from typing import Dict


class Validate:
    """
    Has miscillineous methods for validation

    """

    @staticmethod
    def validate_what3word(input_string: str) -> str:
        """
        Validates that a string is delimited by two "." with three words.

        :param input_string: The string to be validated.
        :return: the input string if valid else raises an error
        """

        if input_string is None or "":
            return ""
        # Split the string using "." as a delimiter
        parts = input_string.split(".")

        # Check if there are exactly three parts
        if len(parts) == 3 and all(part.strip() for part in parts):
            return input_string
        else:
            raise ValueError("Location should be a string of three words delimited with two periods.")

    @staticmethod
    def validate_solar_heat_gain_coefficient(value: float) -> float:
        if 0 <= value <= 1:
            return value
        else:
            raise ValueError("Solar Heat Gain Coefficient must be a float between 0 and 1.")

    @staticmethod
    def validate_none(attributes: Dict):
        none_variables = ""

        for attribute_name, attribute_type in attributes.items():
            if attribute_type is None:
                none_variables = none_variables + attribute_name + " "

        if none_variables:
            raise ValueError("{0} is/are mandatory".format(none_variables.rstrip()))

