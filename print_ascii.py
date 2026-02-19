#!/usr/bin/env python3
# from maze import Cell
# from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from typing import List, Dict
from render_maze import RenderMaze, RenderMazeGenerator, RCell
from mazegen import Maze

# if TYPE_CHECKING:
#     from mazegen import Maze


@dataclass
class AsciiKit:
    """Holds configuration for printing an ASCII maze.

    This class stores foreground and background colours, cell width,
    and box-drawing characters (corners, horizontal, vertical lines)
    used to render the maze in the terminal.
    """
    foreground_colour_list: List[str]
    background_colour_list: List[str]

    # Box drawing characters (class-level constants)
    HOR: str = "━"
    VER: str = "┃"

    TL: str = "┏"
    TR: str = "┓"
    BL: str = "┗"
    BR: str = "┛"

    T_UP: str = "┻"
    T_DOWN: str = "┳"
    T_LEFT: str = "┫"
    T_RIGHT: str = "┣"

    CROSS: str = "╋"

    # # Double-line box drawing characters (class-level constants)
    # HOR: str = "═"
    # VER: str = "║"

    # TL: str = "╔"
    # TR: str = "╗"
    # BL: str = "╚"
    # BR: str = "╝"

    # T_UP: str = "╩"      # tee pointing up
    # T_DOWN: str = "╦"    # tee pointing down
    # T_LEFT: str = "╣"    # tee pointing left
    # T_RIGHT: str = "╠"   # tee pointing right

    # CROSS: str = "╬"

    cell_width: int = 3

    background_path: str = field(init=False)
    background_42: str = field(init=False)
    background_entry: str = field(init=False)
    background_exit: str = field(init=False)
    wall_colour: str = field(init=False)
    reset: str = "\033[0m"

    def __post_init__(self) -> None:
        """Initializes computed fields for background and wall colours."""
        self.background_path = self.background_colour_list[0]
        self.background_42 = self.background_colour_list[1]
        self.background_entry: str = self.background_colour_list[2]
        self.background_exit: str = self.background_colour_list[3]
        self.wall_colour = self.foreground_colour_list[0]


class AsciiPrinter:
    """Manages ASCII maze printing configuration and colour rotation.

    This class stores default foreground and background ANSI colours,
    controls whether the shortest path is displayed, and allows rotation
    of the colour lists for varied output.

    Attributes:
        foreground_colours (List[str]): List of ANSI codes for foreground
            colours.
        background_colours (List[str]): List of ANSI codes for background
            colours.
        include_path (bool): Whether to render the shortest path in the maze.

    Methods:

    """

    def __init__(self) -> None:
        """Initializes the ASCII printer with default colours and path
            visibility."""
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

    @staticmethod
    def render_str(kit: AsciiKit) -> Dict[tuple[str, str], str]:
        """Generates a mapping of cell types and states to their ASCII render
            strings.

        This function converts logical cell types and states into their
        corresponding ASCII characters with ANSI colour codes, based on the
        provided `AsciiKit`. It includes walls, corners, center cells, and
        path/blocked/open states.

        Args:
            kit (AsciiKit): The ASCII kit containing colours, box characters,
                            and cell width for rendering.

        Returns:
            Dict[tuple[str, str], str]: A dictionary mapping `(type, state)`
            tuples to formatted strings ready for printing in the terminal.
        """
        hor_space: str = " " * kit.cell_width
        hor_wall: str = kit.HOR * kit.cell_width

        return {
            ("hor", "wall"): f"{kit.wall_colour}{hor_wall}{kit.reset}",
            ("hor", "open"): f"{hor_space}",
            ("hor", "blocked"): f"{kit.background_42}{hor_space}{kit.reset}",
            ("hor", "path"): f"{kit.background_path}{hor_space}{kit.reset}",

            ("ver", "wall"): f"{kit.wall_colour}{kit.VER}{kit.reset}",
            ("ver", "open"): " ",
            ("ver", "blocked"): f"{kit.background_42} {kit.reset}",
            ("ver", "path"): f"{kit.background_path} {kit.reset}",

            ("center", "open"): f"{hor_space}",
            ("center", "blocked"): f"{
                kit.background_42}{hor_space}{kit.reset}",
            ("center", "path"): f"{kit.background_path}{hor_space}{kit.reset}",
            ("center", "entry"): f"{
                kit.background_entry}{hor_space}{kit.reset}",
            ("center", "exit"): f"{kit.background_exit}{hor_space}{kit.reset}",

            ("corner", "tl"): f"{kit.wall_colour}{kit.TL}{kit.reset}",
            ("corner", "tr"): f"{kit.wall_colour}{kit.TR}{kit.reset}",
            ("corner", "bl"): f"{kit.wall_colour}{kit.BL}{kit.reset}",
            ("corner", "br"): f"{kit.wall_colour}{kit.BR}{kit.reset}",
            ("corner", "t_up"): f"{kit.wall_colour}{kit.T_UP}{kit.reset}",
            ("corner", "t_down"): f"{kit.wall_colour}{kit.T_DOWN}{kit.reset}",
            ("corner", "t_left"): f"{kit.wall_colour}{kit.T_LEFT}{kit.reset}",
            ("corner", "t_right"): (
                f"{kit.wall_colour}{kit.T_RIGHT}{kit.reset}"
                ),
            ("corner", "cross"): f"{kit.wall_colour}{kit.CROSS}{kit.reset}",
            ("corner", ""): " ",  # CornerType.NONE
            ("corner", "hor"): f"{kit.wall_colour}{kit.HOR}{kit.reset}",
            ("corner", "ver"): f"{kit.wall_colour}{kit.VER}{kit.reset}",
        }

    def cell_to_key(self, cell: RCell) -> tuple[str, str]:
        """Converts an RCell into a tuple key representing its type and state.

        This key is used by `render_str` to determine the correct ASCII
        character and colour for the cell. It accounts for horizontal,
        vertical, center, and corner cells, and optionally includes the path
        if `include_path` is enabled.

        Args:
            cell (RCell): The rendered cell whose type and state are to be
            converted.

        Returns:
            tuple[str, str]: A `(type, state)` tuple suitable as a dictionary
            key for ASCII rendering, e.g., `("hor", "wall")` or
            `("corner", "tl")`.
        """
        if cell.horizontal:
            if cell.blocked:
                return ("hor", "blocked")
            elif cell.path:
                if self.include_path is True:
                    return ("hor", "path")
                else:
                    return ("hor", "open")
            elif cell.open:
                return ("hor", "open")
            else:
                return ("hor", "wall")

        elif cell.vertical:
            if cell.blocked:
                return ("ver", "blocked")
            elif cell.path:
                if self.include_path is True:
                    return ("ver", "path")
                else:
                    return ("ver", "open")
            elif cell.open:
                return ("ver", "open")
            else:
                return ("ver", "wall")

        elif cell.center:
            if cell.blocked:
                return ("center", "blocked")
            elif cell.path:
                if self.include_path is True:
                    return ("center", "path")
                else:
                    return ("center", "open")
            elif cell.exit:
                return ("center", "exit")
            # elif cell.open:
            #     return ("center", "open")
            elif cell.entry:
                return ("center", "entry")
            elif cell.exit:
                return ("center", "exit")
            else:
                return ("center", "open")
        else:
            corner_type: str = cell.corner_type.value
        return ("corner", corner_type)

    def rotate_colours(self) -> None:
        """Rotates colour list to the left"""
        self.foreground_colours = self.foreground_colours[
            1:] + self.foreground_colours[:1]

        self.background_colours = self.background_colours[
            1:] + self.background_colours[:1]
        # self.colours[1:] → everything except the first element
        # self.colours[:1] → the first element

    def toggle_path(self) -> None:
        """Toggles the visibility of the shortest path in the ASCII maze.
        If `include_path` is True, it becomes False, and vice versa.
        """
        self.include_path = not self.include_path

    def print_maze(self, maze: "Maze") -> None:
        """Renders a Maze object as ASCII output in the terminal.

        Converts the logical maze into a RenderMaze of RCells, maps each cell
        to its corresponding ASCII character using the current AsciiKit, and
        prints the maze row by row. Uses the foreground and background colours
        defined in the printer, and respects the `include_path` setting.

        Args:
            maze (Maze): The logical Maze object to render.
        """
        kit: AsciiKit = AsciiKit(
            self.foreground_colours, self.background_colours)
        r_maze_generator: RenderMazeGenerator = RenderMazeGenerator()
        r_maze: RenderMaze = r_maze_generator.create(maze)
        output_dict: Dict[tuple[str, str], str] = self.render_str(kit)

        for row in r_maze.grid:
            for cell in row:
                key: tuple[str, str] = self.cell_to_key(cell)
                print(output_dict.get(key, "X"), end="")
            print()
