#   Metadata:
__version__ = "1.0.0"       # Which version of the package
__author__ = "kimendon, sukerl"    # Authors name...duh

#   Imports:
#   The modules/classes/functions you want to expose at the package level.
from .config_parser import ConfigParser, Config
from .errors import ConfigFileError, MazeGeneratorError
from .maze_42 import maze_42
from .maze_generator import MazeGenerator
from .maze import Maze, Cell

# This tells other users what files are "public" and useable/visible
# when the package is imported:
__all__ = [
    "ConfigParser",
    "Config",
    "ConfigFileError",
    "MazeGeneratorError",
    "maze_42",
    "MazeGenerator",
    "Maze",
    "Cell"]
