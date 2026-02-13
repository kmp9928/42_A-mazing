#!/usr/bin/env python3

# from dataclasses import dataclass
from pathlib import Path
# from typing import List
from config_parser import Config
from maze import Cell
from maze_generator import Maze


# @dataclass
# class Cell():
#     north: bool = True
#     east: bool = True
#     south: bool = True
#     west: bool = True
#     charted: bool = True


def convert_cell_to_hex_digit(cell: Cell) -> str:
    """
    Encode a Cell's directional flags (north, east, south, west) as a single
    uppercase hex digit.

    Each direction is treated as a 1-bit value and combined into a 4-bit
    integer:
    west → bit 3, south → bit 2, east → bit 1, north → bit 0.

    Parameters:
        cell (Cell): A Cell with 'north', 'east', 'south', 'west'
        attributes (0 or 1).

    Returns:
        str: Uppercase hexadecimal digit representing the 4 directional bits.
    """

    bit: int = 0
    bit |= (cell.west & 1)
    bit = bit << 1 | (cell.south & 1)
    bit = bit << 1 | (cell.east & 1)
    bit = bit << 1 | (cell.north & 1)
    hex_digit: str = format(bit, "X")
    return hex_digit    # does raising errors here make sense or redundant?


def create_output_txt(maze: Maze, config_obj: Config) -> None:
    """
    Write a textual representation of the maze and configuration to a file.

    The maze is output as a grid of hexadecimal digits, where each Cell is
    converted to a single hex digit using `convert_cell_to_hex_digit`.
    After the maze, the entry and exit coordinates from the configuration
    object are printed. The fastest path to exit is added last.

    Parameters:
        maze (List[List[Cell]]): A 2D list representing the maze grid of Cell
        objects.
        config_obj (Config): Configuration object containing `entry` and `exit`
        coordinates.
        path?????????
    """
    file_path: Path = Path("output_maze.txt")   # add actual path!

    try:
        with open(file_path, "w",  encoding="utf-8") as file:
            for row in maze.grid:
                for cell in row:
                    file.write(f"{convert_cell_to_hex_digit(cell)}")
                file.write("\n")

            file.write("\n")
            file.write(f"{config_obj.entry[0]}, {config_obj.entry[1]}")
            file.write(f"{config_obj.exit[0]}, {config_obj.exit[1]}")
            file.write("here goes fastest path")  # how is it safed and where?
            # do we need to pass it to the function aswelll or part of other
            # object?

    except OSError as err:
        raise OSError(f"ERROR while opening output_maze.txt: {err}")
    #   are other errors redundant since the objects passed should have been
    # checked already..
