#!/usr/bin/env python3

from maze_generator import Maze
from dataclasses import dataclass, field
from typing import List


@dataclass
class AsciiKit:
    """
    holds information needed to print the ASCII grid.
    e.g. colours and what boxcharacters to use
    """
    colour_list: List[str]
    hor_wall: str = "━"
    ver_wall: str = "┃"
    cell_width: int = 3

    background_path: str = field(init=False)
    background_42: str = field(init=False)
    wall_colour: str = field(init=False)
    reset: str = field(init=False)

    def __post_init__(self) -> None:
        self.background_path = self.colour_list[1]
        self.background_42 = self.colour_list[2]
        self.wall_colour = self.colour_list[0]
        self.reset = self.wall_colour


class AsciiPrinter:
    def __init__(self) -> None:
        self.colours: List[str] = ["\033[37m", "\033[40m", "\033[41m"]
        self.include_path: bool = False

    def rotate_colours(self) -> None:
        """rotates colour list to the left"""
        self.colours = self.colours[1:] + self.colours[:1]
        # self.colours[1:] → everything except the first element
        # self.colours[:1] → the first element

    def toggle_path(self) -> None:
        """toggles "show shortest path state"""
        self.include_path = not self.include_path

    def print_maze(self, maze: Maze) -> None:
        """
        Render a maze as ASCII art in the terminal.

        The maze is printed row by row using box-drawing characters to
        represent walls. Each cell displays its north and west walls,
        while the bottom walls are printed after the final row. Cell
        interiors can be filled to indicate special states such as the
        solution path or the "42" pattern.

        The visual appearance (wall characters, colours, cell width) is defined
        by an AsciiKit instance created from the printer's current colour
        scheme.

        Path display can be toggled on or off via the include_path attribute.

        Args:
            maze (Maze): Maze object containing a grid of cells with wall and
                display metadata.

        """
        kit: AsciiKit = AsciiKit(self.colours)
        for row in maze.grid:
            # prints the top of the row, checks for open north only
            for cell in row:
                print(f"{kit.wall_colour}{kit.ver_wall}", end="")
                if cell.north == 1:
                    print(f"{kit.hor_wall*kit.cell_width}", end="")
            print(f"{kit.wall_colour}{kit.ver_wall}{kit.reset}")

            # prints center colours: path, 42 or nothing; checks for open west
            for cell in row:
                if cell.west == 1:
                    print(
                        f"{kit.wall_colour}{kit.ver_wall}{kit.reset}", end=""
                    )
                if cell.is_42 is True:
                    print(
                        f"{kit.background_42}{' '*kit.cell_width}{kit.reset}",
                        end=""
                    )
                elif cell.is_path is True and self.include_path is True:
                    print(
                        f"{kit.background_path}{' '*kit.cell_width}"
                        f"{kit.reset}", end=""
                    )
                else:
                    print(f"{' '*kit.cell_width}", end="")
            print(f"{kit.wall_colour}{kit.ver_wall}{kit.reset}")

        # print bottom row
        for cell in row:
            print(f"{kit.wall_colour}{kit.ver_wall}", end="")
            print(f"{kit.hor_wall}", end="")
        print(f"{kit.wall_colour}{kit.ver_wall}{kit.reset}")
