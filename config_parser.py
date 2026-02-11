from typing import Optional
from dataclasses import dataclass
from pathlib import Path
from class_errors import (
    ConfigFileNotFoundError,
    WrongValueError,
    KeyValueError,
    SyntaxError,
    DimensionsError,
    PointBoundError,
    EntryExitError,
    MandatoryKeyError
)


@dataclass
class Config():
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    # display_mode: str = ASCII

    def __post_init__(self):
        self.validate_dimensions()
        self.validate_entry()
        self.validate_exit()
        self.check_entry_vs_exit()

    def validate_dimensions(self) -> None:
        # If there’s no decision to make, it’s not a maze -> min 2x2
        if self.width < 2:
            raise DimensionsError("WIDTH", self.width)
        if self.height < 2:
            raise DimensionsError("HEIGHT", self.height)

    def validate_entry(self) -> None:
        if (self.entry[0] < 0 or self.entry[0] > self.width - 1 or
           self.entry[1] < 0 or self.entry[1] > self.height - 1):
            raise PointBoundError("ENTRY", self.entry)

    def validate_exit(self) -> None:
        if (self.exit[0] < 0 or self.exit[0] > self.width - 1 or
           self.exit[1] < 0 or self.exit[1] > self.height - 1):
            raise PointBoundError("EXIT", self.exit)

    def check_entry_vs_exit(self) -> None:
        if self.entry[0] == self.exit[0] and self.entry[1] == self.exit[1]:
            raise EntryExitError(self.entry, self.exit)


class ConfigParser():
    @staticmethod
    def load(file_name: str) -> Config:
        data: dict[str, str] = {}
        try:
            with open(file_name, "r") as file:
                for line in file:
                    elements = line.split("=")
                    if len(elements) != 2:
                        raise KeyValueError(line.strip("\n"))
                    data[elements[0]] = elements[1]
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
    def parse_coordinate(is_entry: bool, data: str) -> tuple[int, int]:
        name = "ENTRY"
        if not is_entry:
            name = "EXIT"
        coordinate = data.split(",")
        if len(coordinate) != 2:
            raise SyntaxError(name, data.strip("\n"), "in (x,y) format")
        return (int(coordinate[0]), int(coordinate[1]))

    @staticmethod
    def parse_file_name(name: str, data: str) -> str:
        file_name = data.strip("\n")
        if Path(file_name).suffix != ".txt":
            raise SyntaxError(
                name, file_name, "of '.txt' extension"
            )
        return (file_name)

    @staticmethod
    def parse_bool(data: str) -> bool:
        condition = data.strip("\n").capitalize()
        if condition == "True":
            return True
        if condition == "False":
            return False
        raise SyntaxError("PERFECT", condition, "True or False")

    @staticmethod
    def parse_seed(data: dict[str, str]) -> Optional[int]:
        if data.get("SEED") is not None:
            return (int(data["SEED"]))
