from typing import List
from .maze import Coordinate


class ConfigFileError(Exception):
    """Base class for all configuration file related errors."""
    pass


class ConfigFileNotFoundError(ConfigFileError):
    """Raised when the specified configuration file cannot be found.

    Attributes:
        file (str): Path of the missing file.
    """
    def __init__(self, file: str):
        super().__init__(f"Wrong config file. {file} doesn't exist.")


class WrongValueError(ConfigFileError):
    """Raised when a value in the config file cannot be converted to a number.

    Attributes:
        value (str): The invalid value from the config file.
    """
    def __init__(self, value: str):
        super().__init__(f"Value {value} is not a number.")


class KeyValueError(ConfigFileError):
    """Raised when a configuration file line is not in 'KEY=VALUE' format.

    Attributes:
        pair (str): The invalid line from the configuration file.
    """
    def __init__(self, pair: str):
        super().__init__(
            "Configuration file must contain one 'KEY=VALUE' pair per line. " +
            f"Please check '{pair}'."
        )


class SyntaxError(ConfigFileError):
    """Raised when a configuration parameter has an invalid value or format.

    Attributes:
        parameter (str): Name of the parameter.
        value (int): Value of the parameter.
        condition (str): Required condition for the parameter.
    """
    def __init__(self, parameter: str, value: int, condition: str):
        super().__init__(
            f"{parameter} with value {value} not valid. " +
            f"Parameter must be {condition}."
        )


class DimensionsError(ConfigFileError):
    """Raised when maze dimensions are invalid (less than minimum allowed).

    Attributes:
        parameter (str): Name of the dimension parameter ('WIDTH' or 'HEIGHT').
        value (int): Provided dimension value.
    """
    def __init__(self, parameter: str, value: int):
        super().__init__(
            f"Maze {parameter} can't be {value}, must be at least 2."
        )


class PointBoundError(ConfigFileError):
    """Raised when a coordinate (entry or exit) is outside the maze bounds.

    Attributes:
        parameter (str): Name of the parameter ('ENTRY' or 'EXIT').
        value (int): Coordinate value that is out of bounds.
    """
    def __init__(self, parameter: str, value: int):
        super().__init__(
            f"{parameter} not valid. {value} must be inside the maze bounds."
        )


class EntryExitError(ConfigFileError):
    """Raised when entry and exit points are identical.

    Attributes:
        entry (str): Entry coordinate.
        exit (int): Exit coordinate.
    """
    def __init__(self, entry: str, exit: int):
        super().__init__(
            f"Invalid entry {entry} and exit {exit}. Points must be different."
        )


class MandatoryKeyError(ConfigFileError):
    """Raised when a mandatory key is missing from the configuration file.

    Attributes:
        key (str): Name of the missing key.
    """
    def __init__(self, key: str):
        super().__init__(f"Missing mandatory key {key} in configuration file.")


class MazeGeneratorError(Exception):
    """Base class for all maze generator related errors."""
    pass


class EntryExitInFTError(MazeGeneratorError):
    """Raised when entry or exit coordinates overlap with the '42' pattern.

    Attributes:
        patter (List[Coordinate]): List of coordinates of the '42' pattern.
    """
    def __init__(self, pattern: List[Coordinate]):
        super().__init__(
            "Entry/exit in '42' pattern. For this maze, entry/exit points " +
            f"can't be any of these coordinates: {pattern}")
