#!/usr/bin/env python3
# from maze import Cell
from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from typing import List

if TYPE_CHECKING:
    from mazegen import Maze


@dataclass
class AsciiKit:
    """
    holds information needed to print the ASCII grid.
    e.g. colours and what boxcharacters to use
    """
    foreground_colour_list: List[str]
    background_colour_list: List[str]
    hor_wall: str = "━"
    ver_wall: str = "┃"
    cell_width: int = 3

    background_path: str = field(init=False)
    background_42: str = field(init=False)
    wall_colour: str = field(init=False)
    reset: str = "\033[0m"

    def __post_init__(self) -> None:
        self.background_path = self.background_colour_list[0]
        self.background_42 = self.background_colour_list[1]
        self.wall_colour = self.foreground_colour_list[0]
        # self.reset = "\033[0m"


class AsciiPrinter:
    def __init__(self) -> None:
        self.foreground_colours: List[str] = [
            "\033[37m",  # white
            "\033[33m",  # yellow
            "\033[36m",  # cyan
        ]
        self.background_colours: List[str] = [
            "\033[44m",  # blue
            "\033[45m",  # magenta
            "\033[42m",  # green
            "\033[41m",  # red
        ]
        self.include_path: bool = False

    def rotate_colours(self) -> None:
        """rotates colour list to the left"""
        self.foreground_colours = self.foreground_colours[
            1:] + self.foreground_colours[:1]

        self.background_colours = self.background_colours[
            1:] + self.background_colours[:1]
        # self.colours[1:] → everything except the first element
        # self.colours[:1] → the first element

    def toggle_path(self) -> None:
        """toggles "show shortest path state"""
        self.include_path = not self.include_path

    def print_maze(self, maze: "Maze") -> None:
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
        kit: AsciiKit = AsciiKit(
            self.foreground_colours, self.background_colours)
        for row in maze.grid:
            # prints the top of the row, checks for open north only
            for cell in row:
                print(f"{kit.wall_colour}{kit.ver_wall}", end="")
                if cell.north is True:
                    print(f"{kit.hor_wall*kit.cell_width}", end="")
                else:
                    print(" "*kit.cell_width, end="")
            print(f"{kit.wall_colour}{kit.ver_wall}{kit.reset}")

            # prints center colours: path, 42 or nothing; checks for open west
            for cell in row:
                if cell.west is True:
                    print(
                        f"{kit.wall_colour}{kit.ver_wall}{kit.reset}", end=""
                    )
                else:
                    print(" ", end="")
                if cell.blocked is True:
                    print(
                        f"{kit.background_42}{' '*kit.cell_width}{kit.reset}",
                        end=""
                    )
                elif cell.path is True and self.include_path is True:
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
            print(f"{kit.hor_wall*kit.cell_width}", end="")
        print(f"{kit.wall_colour}{kit.ver_wall}{kit.reset}")
