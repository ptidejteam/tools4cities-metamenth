class Validate:
    """A class with a static method for string validation."""

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
