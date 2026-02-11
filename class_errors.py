class ConfigFileError(Exception):
    pass


class ConfigFileNotFoundError(ConfigFileError):
    def __init__(self, file: str):
        super().__init__(f"Wrong config file. {file} doesn't exist.")


class WrongValueError(ConfigFileError):
    def __init__(self, value: str):
        super().__init__(f"Value {value} is not a number.")


class KeyValueError(ConfigFileError):
    def __init__(self, pair: str):
        super().__init__(
            "Configuration file must contain one 'KEY=VALUE' pair per line. " +
            f"Please check '{pair}'."
        )


class SyntaxError(ConfigFileError):
    def __init__(self, parameter: str, value: int, condition: str):
        super().__init__(
            f"{parameter} with value {value} not valid. " +
            f"Parameter must be {condition}."
        )


class DimensionsError(ConfigFileError):
    def __init__(self, parameter: str, value: int):
        super().__init__(
            f"Maze {parameter} can't be {value}, must be at least 2."
        )


class PointBoundError(ConfigFileError):
    def __init__(self, parameter: str, value: int):
        super().__init__(
            f"{parameter} not valid. {value} must be inside the maze bounds."
        )


class EntryExitError(ConfigFileError):
    def __init__(self, entry: str, exit: int):
        super().__init__(
            f"Invalid entry {entry} and exit {exit}. Points must be different."
        )


class MandatoryKeyError(ConfigFileError):
    def __init__(self, key: str):
        super().__init__(f"Missing mandatory key {key} in configuration file.")
