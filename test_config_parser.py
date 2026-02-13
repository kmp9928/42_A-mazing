import os
import pytest
from typing import Union, Optional
from config_parser import ConfigParser, Config
from errors import ConfigFileError


def prepare_test_file(override: Optional[Union[dict[str, str], str]]):
    to_write = {
        "WIDTH": "20",
        "HEIGHT": "15",
        "ENTRY": "0,0",
        "EXIT": "19,14",
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": "True"
    }
    if isinstance(override, dict):
        for key, value in override.items():
            if key in to_write:
                to_write.update(override)
            else:
                to_write[key] = value
    elif isinstance(override, str):
        del to_write[override]
    with open("test_config.txt", "w") as file:
        for key, value in to_write.items():
            file.write(key + "=" + value + "\n")


@pytest.mark.parametrize("expected_error", [
    ("Wrong config file. 'invalid_config.txt' doesn't exist.")
])
def test_invalid_config_file(expected_error):
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("invalid_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("width,expected_error", [
    ("3=1", "Configuration file must contain one 'KEY=VALUE' pair per line. Please check 'WIDTH=3=1'.")
])
def test_invalid_key_value(width, expected_error):
    prepare_test_file({"WIDTH": width})
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("width,expected_error", [
    ("a", "Value 'a\\n' is not a number."),
    ("-1", "Maze WIDTH can't be -1, must be at least 2."),
    ("1", "Maze WIDTH can't be 1, must be at least 2.")
])
def test_invalid_width(width, expected_error):
    prepare_test_file({"WIDTH": width})
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("height,expected_error", [
    ("abc", "Value 'abc\\n' is not a number."),
    ("-3", "Maze HEIGHT can't be -3, must be at least 2."),
    ("0", "Maze HEIGHT can't be 0, must be at least 2.")
])
def test_invalid_height(height, expected_error):
    prepare_test_file({"HEIGHT": height})
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("entry,expected_error", [
    ("k", "ENTRY with value k not valid. Parameter must be in (x,y) format."),
    ("4", "ENTRY with value 4 not valid. Parameter must be in (x,y) format."),
    ("a,1", "Value 'a' is not a number."),
    ("-1,1", "ENTRY not valid. (-1, 1) must be inside the maze bounds."),
    ("1,-1", "ENTRY not valid. (1, -1) must be inside the maze bounds."),
    ("20,10", "ENTRY not valid. (20, 10) must be inside the maze bounds."),
    ("10,15", "ENTRY not valid. (10, 15) must be inside the maze bounds."),
    ("19,14", "Invalid entry (19, 14) and exit (19, 14). Points must be different.")
])
def test_invalid_entry(entry, expected_error):
    prepare_test_file({"ENTRY": entry})
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("exit,expected_error", [
    ("k", "EXIT with value k not valid. Parameter must be in (x,y) format."),
    ("4", "EXIT with value 4 not valid. Parameter must be in (x,y) format."),
    ("a,1", "Value 'a' is not a number."),
    ("-1,1", "EXIT not valid. (-1, 1) must be inside the maze bounds."),
    ("1,-1", "EXIT not valid. (1, -1) must be inside the maze bounds."),
    ("20,10", "EXIT not valid. (20, 10) must be inside the maze bounds."),
    ("10,15", "EXIT not valid. (10, 15) must be inside the maze bounds."),
    ("0,0", "Invalid entry (0, 0) and exit (0, 0). Points must be different.")
])
def test_invalid_exit(exit, expected_error):
    prepare_test_file({"EXIT": exit})
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("output_file,expected_error", [
    ("maze.xls", "OUTPUT_FILE with value maze.xls not valid. Parameter must be of '.txt' extension.")
])
def test_invalid_output_file(output_file, expected_error):
    prepare_test_file({"OUTPUT_FILE": output_file})
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("perfect,expected_error", [
    ("Maybe", "PERFECT with value Maybe not valid. Parameter must be True or False."),
    ("0", "PERFECT with value 0 not valid. Parameter must be True or False."),
    ("Tru", "PERFECT with value Tru not valid. Parameter must be True or False."),

])
def test_invalid_perfect(perfect, expected_error):
    prepare_test_file({"PERFECT": perfect})
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("expected_error", [
    ("Missing mandatory key 'WIDTH' in configuration file.")
])
def test_missing_mandatory_key(expected_error):
    prepare_test_file("WIDTH")
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


@pytest.mark.parametrize("seed,expected_error", [
    ("a", "Value 'a\\n' is not a number.")
])
def test_invalid_seed(seed, expected_error):
    prepare_test_file({"SEED": seed})
    with pytest.raises(ConfigFileError) as e:
        ConfigParser.load("test_config.txt")
    assert str(e.value) == expected_error


def test_valid_config():
    prepare_test_file({"SEED": "1"})
    assert ConfigParser.load("test_config.txt") == Config(width=20, height=15, entry=(0, 0), exit=(19, 14), output_file='maze.txt', perfect=True, seed=1)
    prepare_test_file(None)
    assert ConfigParser.load("test_config.txt") == Config(width=20, height=15, entry=(0, 0), exit=(19, 14), output_file='maze.txt', perfect=True, seed=None)
    os.remove("test_config.txt")
