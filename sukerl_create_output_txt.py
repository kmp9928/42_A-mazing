#!/usr/bin/env python3

# from typing import TYPE_CHECKING
from pathlib import Path
from mazegen import Maze, Config, Cell


class OutputGenerator:
    @staticmethod
    def convert_cell_to_hex_digit(cell: Cell) -> str:
        """
        Encode a Cell's directional flags (north, east, south, west) as a
        single uppercase hex digit.

        Each direction is treated as a 1-bit value and combined into a 4-bit
        integer:
        west → bit 3, south → bit 2, east → bit 1, north → bit 0.

        Parameters:
            cell (Cell): A Cell with 'north', 'east', 'south', 'west'
            attributes (0 or 1).

        Returns:
            str: Uppercase hexadecimal digit representing the 4 directional
            bits.
        """

        bit: int = 0
        bit |= (cell.west & 1)
        bit = bit << 1 | (cell.south & 1)
        bit = bit << 1 | (cell.east & 1)
        bit = bit << 1 | (cell.north & 1)
        hex_digit: str = format(bit, "X")
        return hex_digit    # does raising errors here make sense or redundant?

    def create_output_txt(self, maze: Maze, config_obj: Config) -> None:
        """
        Write a textual representation of the maze and configuration to a file.

        The maze is output as a grid of hexadecimal digits, where each Cell is
        converted to a single hex digit using `convert_cell_to_hex_digit`.
        After the maze, the entry and exit coordinates from the configuration
        object are printed. The fastest path to exit is added last.

        Parameters:
            maze (List[List[Cell]]): A 2D list representing the maze grid of
            Cell objects.
            config_obj (Config): Configuration object containing `entry` and
            `exit` coordinates.
            path?????????
        """
        file_name = config_obj.output_file
        file_path: Path = Path(file_name)   # add actual path!

        try:
            with open(file_path, "w",  encoding="utf-8") as file:
                for row in maze.grid:
                    for cell in row:
                        file.write(f"{self.convert_cell_to_hex_digit(cell)}")
                    file.write("\n")

                file.write("\n")
                file.write(f"{config_obj.entry[0]},{config_obj.entry[1]}\n")
                file.write(f"{config_obj.exit[0]},{config_obj.exit[1]}\n")
                file.write("here goes fastest path")

        except OSError as err:
            raise OSError(f"ERROR while opening {file_name}: {err}")
