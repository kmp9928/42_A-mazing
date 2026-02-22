from typing import Optional
from dataclasses import dataclass
from pathlib import Path
from .errors import (
    ConfigFileNotFoundError,
    WrongValueError,
    KeyValueError,
    SyntaxError,
    DimensionsError,
    PointBoundError,
    EntryExitError,
    MandatoryKeyError
)
from typing import List


@dataclass
class Config():
    """Store and validate maze configuration parameters.

    This class represents the validated configuration used for maze
    generation, including dimensions, entry/exit coordinates,
    output file name, generation mode and optional seed.

    Validation is automatically performed after initialization.

    Attributes:
        width (int): Maze width (number of columns).
        height (int): Maze height (number of rows).
        entry (tuple[int, int]): Entry coordinate (x, y).
        exit (tuple[int, int]): Exit coordinate (x, y).
        output_file (str): Output file path for maze export.
        perfect (bool): Whether the maze should be perfect
            (with only one solution and no loops).
        seed (Optional[int]): Random seed for reproducibility.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    # display_mode: str = ASCII

    def __post_init__(self):
        """Validate configuration values after initialization.

        Calls all validation methods to ensure:
            - Dimensions are valid.
            - Entry and exit are within bounds.
            - Entry and exit are not identical.
        """
        self.validate_dimensions()
        self.validate_entry()
        self.validate_exit()
        self.check_entry_vs_exit()

    def validate_dimensions(self) -> None:
        """Validate maze dimensions.

        Ensures the maze has at least 2 rows and 2 columns (if there are no
        decision to make, it is not a maze).

        Raises:
            DimensionsError: If width or height is less than 2.
        """
        if self.width < 2:
            raise DimensionsError("WIDTH", self.width)
        if self.height < 2:
            raise DimensionsError("HEIGHT", self.height)

    def validate_entry(self) -> None:
        """Validate that the entry coordinate is within maze bounds.

        Raises:
            PointBoundError: If the entry coordinate is outside
                the maze dimensions.
        """
        if (self.entry[0] < 0 or self.entry[0] > self.width - 1 or
           self.entry[1] < 0 or self.entry[1] > self.height - 1):
            raise PointBoundError("ENTRY", self.entry)

    def validate_exit(self) -> None:
        """Validate that the exit coordinate is within maze bounds.

        Raises:
            PointBoundError: If the exit coordinate is outside
                the maze dimensions.
        """
        if (self.exit[0] < 0 or self.exit[0] > self.width - 1 or
           self.exit[1] < 0 or self.exit[1] > self.height - 1):
            raise PointBoundError("EXIT", self.exit)

    def check_entry_vs_exit(self) -> None:
        """Ensure entry and exit are not the same coordinate.

        Raises:
            EntryExitError: If entry and exit coordinates are identical.
        """
        if self.entry[0] == self.exit[0] and self.entry[1] == self.exit[1]:
            raise EntryExitError(self.entry, self.exit)


class ConfigParser():
    """Parse configuration files and construct Config objects.

    This class reads key-value pairs from a configuration file,
    validates required fields, converts values to appropriate types,
    and returns a fully validated Config instance.
    """
    @staticmethod
    def load(file_name: str) -> Config:
        """Load configuration from a file.

        The file must contain key=value pairs for all mandatory fields:
        WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT.
        SEED is optional.

        Args:
            file_name (str): Path to the configuration file.

        Returns:
            Config: Validated configuration object.

        Raises:
            ConfigFileNotFoundError: If the file does not exist.
            MandatoryKeyError: If a required key is missing.
            WrongValueError: If a value cannot be converted properly.
            KeyValueError: If a line is not in key=value format.
        """
        data: dict[str, str] = {}
        try:
            with open(file_name, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key_value = ConfigParser.get_key_value(line)
                    if len(key_value) != 2:
                        raise KeyValueError(line)
                    data[key_value[0].strip()] = key_value[1].strip()
                return Config(
                    width=int(data["WIDTH"]),
                    height=int(data["HEIGHT"]),
                    entry=ConfigParser.parse_coordinate(True, data["ENTRY"]),
                    exit=ConfigParser.parse_coordinate(False, data["EXIT"]),
                    output_file=ConfigParser.parse_file_name(
                        "OUTPUT_FILE", data["OUTPUT_FILE"]
                    ),
                    perfect=ConfigParser.parse_bool(data["PERFECT"]),
                    seed=ConfigParser.parse_seed(data)
                )
        except FileNotFoundError as e:
            raise ConfigFileNotFoundError(str(e).split(": ")[1])
        except ValueError as e:
            raise WrongValueError(str(e).split(": ")[1])
        except KeyError as e:
            raise MandatoryKeyError(e)

    @staticmethod
    def get_key_value(line: str) -> List[str]:
        """Extract a key-value pair from a line from the configuration file.

        This function processes a single line from a configuration file,
        ignoring any inline comments (denoted by `#`). It returns the key 
        and value as a list of two strings. The function expects lines in the
        format KEY=VALUE

        Args:
            line (str): A line from the configuration file.

        Returns:
            List[str]: A list containing the key and value as strings.

        Raises:
            KeyValueError: If the line does not contain a valid key-value pair.
        
        Examples:
            >>> get_key_value("WIDTH=10")
            ['WIDTH', '10']
            >>> get_key_value("HEIGHT=20 # height of the maze")
            ['HEIGHT', '20']
        """
        clean_line = line.split("#")
        if len(clean_line) == 1:
            return clean_line[0].split("=")
        else:
            for element in clean_line:
                if "=" in element:
                    return element.strip().split("=")
        raise KeyValueError(line)

    @staticmethod
    def parse_coordinate(is_entry: bool, data: str) -> tuple[int, int]:
        """Parse a coordinate string in (x,y) format.

        Args:
            is_entry (bool): True if parsing ENTRY, False if EXIT.
            data (str): Coordinate string (e.g., "3,4").

        Returns:
            tuple[int, int]: Parsed (x, y) coordinate.

        Raises:
            SyntaxError: If the format is invalid.
            ValueError: If values cannot be converted to integers.
        """
        name = "ENTRY"
        if not is_entry:
            name = "EXIT"
        coordinate = data.split(",")
        if len(coordinate) != 2:
            raise SyntaxError(name, data, "in (x,y) format")
        return (int(coordinate[0]), int(coordinate[1]))

    @staticmethod
    def parse_file_name(name: str, data: str) -> str:
        """Validate and parse output file name.

        Ensures the file has a '.txt' extension.

        Args:
            name (str): Configuration key name.
            data (str): File name string.

        Returns:
            str: Validated file name.

        Raises:
            SyntaxError: If the file extension is not '.txt'.
        """
        file_name = data
        if Path(file_name).suffix != ".txt":
            raise SyntaxError(
                name, file_name, "of '.txt' extension"
            )
        return (file_name)

    @staticmethod
    def parse_bool(data: str) -> bool:
        """Parse a boolean configuration value.

        Accepts 'True' or 'False' (case-insensitive).

        Args:
            data (str): Boolean string value.

        Returns:
            bool: Parsed boolean value.

        Raises:
            SyntaxError: If the value is not 'True' or 'False'.
        """
        if data.capitalize() == "True":
            return True
        if data.capitalize() == "False":
            return False
        raise SyntaxError("PERFECT", data, "True or False")

    @staticmethod
    def parse_seed(data: dict[str, str]) -> Optional[int]:
        """Parse optional random seed value.

        Args:
            data (dict[str, str]): Parsed key-value pairs.

        Returns:
            Optional[int]: Integer seed if provided, otherwise None.

        Raises:
            ValueError: If the seed cannot be converted to an integer.
        """
        if data.get("SEED") is not None:
            return (int(data["SEED"]))
