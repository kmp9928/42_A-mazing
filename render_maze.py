#!/usr/bin/env python3

from typing import List, Any
from enum import Enum
from dataclasses import dataclass
from mazegen import Maze, Cell

# if TYPE_CHECKING:
#     from mazegen import Maze, Cell

# type Coordinate = tuple[int, int]


class RCellType(Enum):
    """Enumeration of render cell types in the rendered maze.

    This enum defines the structural role of an RCell in the rendered maze
    grid. Each original maze cell is expanded into 4 render cells
    representing walls, corners, and the cell interior.

    Attributes:
        VERTICAL: A vertical wall segment.
        HORIZONTAL: A horizontal wall segment.
        CENTER: The interior (center) of a maze cell.
        CORNER: A junction or corner between wall segments.
    """
    VERTICAL = 0
    HORIZONTAL = 1
    CENTER = 2
    CORNER = 3


class CornerType(Enum):
    """Enumeration of corner and junction shapes for rendered maze cells.

    This enum describes the exact box-drawing shape that should be printed
    for an RCell of type CORNER. The value of each enum member is used
    directly as a lookup key in the ASCII rendering map.

    The corner type is determined during render-maze generation based on
    surrounding wall connections.
    """
    HOR = "hor"          # horizontal line
    VER = "ver"          # vertical line
    TL = "tl"            # top-left corner
    TR = "tr"            # top-right corner
    BL = "bl"            # bottom-left corner
    BR = "br"            # bottom-right corner
    T_UP = "t_up"        # tee pointing up (┴)
    T_DOWN = "t_down"    # tee pointing down (┬)
    T_LEFT = "t_left"    # tee pointing left (┤)
    T_RIGHT = "t_right"  # tee pointing right (├)
    CROSS = "cross"      # cross (┼)
    NONE = ""            # not a corner


@dataclass
class RCell:
    """Represents a single rendered cell in the ASCII maze grid.

    An RCell is a *render-level* cell derived from a logical maze Cell.
    Each maze cell is expanded into 4 RCells to represent either a wall,
    corner or interior space for ASCII rendering.

    An RCell has:
    - a structural type (vertical wall, horizontal wall, center, or corner)
    - optional semantic flags (blocked, path, entry, exit, open)
    - an optional CornerType describing which box-drawing character to print

    RCell instances are created by RenderMazeGenerator and later consumed
    by the ASCII printer to determine which characters and colours to output.

    Attributes:
        blocked: True if this rendered cell represents a blocked area.
        path: True if this rendered cell is part of the solution path.
        entry: True if this rendered cell marks the maze entry.
        exit: True if this rendered cell marks the maze exit.
        open: True if this rendered cell represents an open passage.
        type: The structural type of the rendered cell (RCellType).
        corner_type: The specific corner or junction shape to render
            when type is RCellType.CORNER.
    """
    blocked: bool = False
    path: bool = False
    entry: bool = False
    exit: bool = False
    open: bool = False
    type: RCellType = RCellType.CENTER
    corner_type: CornerType = CornerType.NONE

    @property
    def vertical(self) -> bool:
        """Indicates whether this RCell is a vertical wall cell.
        Returns:
            True if the cell type is RCellType.VERTICAL, False otherwise.
        """
        return self.type == RCellType.VERTICAL

    @property
    def horizontal(self) -> bool:
        """Indicates whether this RCell is a horizontal wall cell.
        Returns:
            bool: True if the cell type is RCellType.HORIZONTAL,
            False otherwise.
        """
        return self.type == RCellType.HORIZONTAL

    @property
    def center(self) -> bool:
        """Indicates whether this RCell is a center cell.
        Returns:
            bool: True if the cell type is RCellType.CENTER, False otherwise.
        """
        return self.type == RCellType.CENTER

    @property
    def corner(self) -> bool:
        """Indicates whether this RCell is a corner cell.
        Returns:
            bool: True if the cell type is RCellType.CORNER, False otherwise.
        """
        return self.type == RCellType.CORNER

    # ** -> Collect all keyword arguments (kwargs) passed to this
    # function into a dictionary: can be more than one key value pair
    def set(self, **kwargs: Any) -> "RCell":
        """ Sets the cell properties.
        For example:
        - cell.set(path=True)
        - cell.set(type=CellType.VERTICAL)
        """
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        return self


class RenderMaze:
    """Represents a rendered version of a maze using RCells.

    The rendered maze expands each logical maze cell into a grid of
    RCells that track walls, paths, corners, and open spaces. This
    allows for easy ASCII or graphical rendering of the maze.
    """
    grid: List[List[RCell]]
    width: int
    height: int

    def __init__(self, maze: "Maze") -> None:
        """Initializes the RenderMaze from a Maze object.

        Args:
            maze (Maze): The source maze to render. Its logical cells
                         will be expanded into a grid of RCells.
        """
        self.width = (maze.width * 2) + 1
        self.height = (maze.height * 2) + 1
        self.grid = []

        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(RCell())
            self.grid.append(row)


class RenderMazeGenerator:
    """Generates a RenderMaze from a Maze object.

    This class provides methods to convert a logical maze into a
    rendered grid of RCells suitable for ASCII or graphical output.
    It handles splitting each logical cell into corners, walls, and
    center cells, and allows access to neighboring cells.

    Methods:
        get_top_cell(row, col, maze): Returns the maze cell immediately above
            the given position, or None if at the top row.
        get_prev_cell(row, col, maze): Returns the maze cell immediately to the
            left of the given position, or None if at the leftmost column.
        set_corner(col, top, prev): Creates a corner RCell and assigns its
            corner type based on neighboring cells.
        set_last_col_corner(col): Generates the appropriate corner RCell for
            the last column of a row.
        set_hor_wall(col, top): Creates a horizontal wall RCell based on the
            cell above.
        set_ver_wall(col, prev): Creates a vertical wall RCell based on the
            cell to the left.
        set_center(col): Generates a center RCell reflecting the logical state
            of the maze cell.
        set_last_row(c, maze): Generates the correct RCell for a specific
            column in the last row of the maze.
        create(maze): Builds a complete RenderMaze by converting all logical
            Cells into RCells.
    """

    @staticmethod
    def get_top_cell(row: int, col: int, maze: "Maze") -> Cell | None:
        """Return the cell immediately above a given position.

        Args:
            row (int): Row index of the current cell.
            col (int): Column index of the current cell.
            maze (Maze): Maze object containing the grid.

        Returns:
            Cell | None: The cell above, or None if topmost row.
        """
        if row > 0:
            return maze.grid[row - 1][col]
        return None

    @staticmethod
    def get_prev_cell(row: int, col: int, maze: "Maze") -> Cell | None:
        """Return the cell immediately to the left of a given position.

        Args:
            row (int): Row index of the current cell.
            col (int): Column index of the current cell.
            maze (Maze): Maze object containing the grid.

        Returns:
            Cell | None: The cell to the left, or None if leftmost column.
        """
        if col > 0:
            return maze.grid[row][col - 1]
        return None

    @staticmethod
    def set_corner(col: Cell, top: Cell | None, prev: Cell | None) -> RCell:
        """Create a corner RCell and determine its corner type based on
            neighbors.

        Args:
            col (Cell): The current maze cell.
            top (Cell | None): The cell above, if any.
            prev (Cell | None): The cell to the left, if any.

        Returns:
            RCell: The rendered corner cell.
        """
        rcell: RCell = RCell()
        rcell.set(type=RCellType.CORNER)
        if top is None:
            if prev is None:
                rcell.set(corner_type=CornerType.TL)
            elif prev.east is True:
                rcell.set(corner_type=CornerType.T_DOWN)
            else:
                rcell.set(corner_type=CornerType.HOR)
            return rcell
        if prev is None:
            if col.north is True:
                rcell.set(corner_type=CornerType.T_RIGHT)
            else:
                rcell.set(corner_type=CornerType.VER)
            return rcell
        if col.north is True:
            if prev.north is False:
                if col.west is True and top.west is True:
                    rcell.set(corner_type=CornerType.T_RIGHT)
                elif col.west is True and top.west is False:
                    rcell.set(corner_type=CornerType.TL)
                elif col.west is False and top.west is True:
                    rcell.set(corner_type=CornerType.BL)
            else:
                if col.west is False and top.west is False:
                    rcell.set(corner_type=CornerType.HOR)
                elif col.west is True and top.west is True:
                    rcell.set(corner_type=CornerType.CROSS)
                elif col.west is True and top.west is False:
                    rcell.set(corner_type=CornerType.T_DOWN)
                elif col.west is False and top.west is True:
                    rcell.set(corner_type=CornerType.T_UP)

        else:
            if prev.north is True:
                if col.west is True and top.west is True:
                    rcell.set(corner_type=CornerType.T_LEFT)
                elif col.west is True and top.west is False:
                    rcell.set(corner_type=CornerType.TR)
                elif col.west is False and top.west is True:
                    rcell.set(corner_type=CornerType.BR)
            else:
                if col.west is True and top.west is True:
                    rcell.set(corner_type=CornerType.VER)
        return rcell

    @staticmethod
    def set_last_col_corner(col: Cell) -> RCell:
        """Return a corner cell for the last column based on the north wall.

        Args:
            col (Cell): The current maze cell.

        Returns:
            RCell: The rendered corner cell for the last column.
        """
        rcell: RCell = RCell()
        rcell.set(type=RCellType.CORNER)
        if col.north is True:
            rcell.set(corner_type=CornerType.T_LEFT)
        else:
            rcell.set(corner_type=CornerType.VER)
        return rcell

    # THIS PRINTS 42 BACKGROUND IN CELLS not continuous
    @staticmethod
    def set_hor_wall(col: Cell, top: Cell | None) -> RCell:
        """Return a horizontal wall RCell based on the top neighbor.

        Args:
            col (Cell): The current maze cell.
            top (Cell | None): The cell above, if any.

        Returns:
            RCell: The rendered horizontal wall cell.
        """
        rcell: RCell = RCell()
        rcell.set(type=RCellType.HORIZONTAL)
        if top is None:
            return rcell
        if col.north is False:
            rcell.set(open=True)
            if col.blocked is True and top.blocked is True:
                rcell.set(blocked=True)
            elif col.path is True and top.path is True:
                rcell.set(path=True)
            elif top.entry or top.exit and col.path is True:  #
                rcell.set(path=True)
            elif col.entry or col.exit and top.path is True:  #
                rcell.set(path=True)
        return rcell

    # @staticmethod
    # def set_hor_wall(col: Cell, top: Cell | None) -> RCell:
    #     """Return a horizontal wall RCell based on the top neighbor.

    #     Args:
    #         col (Cell): The current maze cell.
    #         top (Cell | None): The cell above, if any.

    #     Returns:
    #         RCell: The rendered horizontal wall cell.
    #     """
    #     rcell: RCell = RCell()
    #     rcell.set(type=RCellType.HORIZONTAL)
    #     if top is None:
    #         return rcell
    #     if col.north is False:
    #         rcell.set(open=True)
    #         # if col.blocked is True and top.blocked is True:
    #         #     rcell.set(blocked=True)
    #         if col.path is True and top.path is True:
    #             rcell.set(path=True)
    #         elif top.entry or top.exit and col.path is True:  #
    #             rcell.set(path=True)
    #         elif col.entry or col.exit and top.path is True:  #
    #             rcell.set(path=True)
    #     elif col.blocked is True and top.blocked is True:
    #         rcell.set(blocked=True)

    #     return rcell

    # THIS PRINTS 42 BACKGROUND IN CELLS not continuous:
    @staticmethod
    def set_ver_wall(col: Cell, prev: Cell | None) -> RCell:
        """Return a vertical wall RCell based on the left neighbor.

        Args:
            col (Cell): The current maze cell.
            prev (Cell | None): The cell to the left, if any.

        Returns:
            RCell: The rendered vertical wall cell.
        """
        rcell: RCell = RCell()
        rcell.set(type=RCellType.VERTICAL)
        if prev is None:
            return rcell
        if col.west is False:
            rcell.set(open=True)
            if col.blocked is True and prev.blocked is True:
                rcell.set(blocked=True)
            elif col.path is True and prev.path is True:
                rcell.set(path=True)
            elif col.exit or col.entry and prev.path is True:  #
                rcell.set(path=True)
            elif col.path is True and prev.entry or prev.exit:  # #
                rcell.set(path=True)
        return rcell

    # @staticmethod
    # def set_ver_wall(col: Cell, prev: Cell | None) -> RCell:
    #     """Return a vertical wall RCell based on the left neighbor.

    #     Args:
    #         col (Cell): The current maze cell.
    #         prev (Cell | None): The cell to the left, if any.

    #     Returns:
    #         RCell: The rendered vertical wall cell.
    #     """
    #     rcell: RCell = RCell()
    #     rcell.set(type=RCellType.VERTICAL)
    #     if prev is None:
    #         return rcell
    #     if col.west is False:
    #         rcell.set(open=True)
    #         if col.blocked is True and prev.blocked is True:
    #             rcell.set(blocked=True)
    #         elif col.path is True and prev.path is True:
    #             rcell.set(path=True)
    #         elif (col.exit or col.entry) and prev.path is True:  #
    #             rcell.set(path=True)
    #         elif col.path is True and (prev.entry or prev.exit):  # #
    #             rcell.set(path=True)
    #     if col.blocked is True and prev.blocked is True:
    #         rcell.set(blocked=True)
    #     return rcell

    @staticmethod
    def set_center(col: Cell) -> RCell:
        """Return a center RCell based on the logical cell type.

        Args:
            col (Cell): The current maze cell.

        Returns:
            RCell: The rendered center cell.
        """
        rcell: RCell = RCell()
        rcell.set(type=RCellType.CENTER)
        if col.blocked is True:
            rcell.set(blocked=True)
        elif col.path is True:
            rcell.set(path=True)
        elif col.entry is True:
            rcell.set(entry=True)
        elif col.exit is True:
            rcell.set(exit=True)
        return rcell

    def set_last_row(self, c: int, maze: "Maze") -> RCell:
        """Return the correct RCell for a given position in the last row.

        Args:
            c (int): Column index in the rendered grid.
            maze (Maze): The source maze.

        Returns:
            RCell: The rendered cell for the last row.
        """
        rcell: RCell = RCell()

        if c % 2 == 0:
            rcell.set(type=RCellType.CORNER)
        else:
            rcell.set(type=RCellType.HORIZONTAL)

        # Bottom left corner:
        if c == 0:
            rcell.set(corner_type=CornerType.BL)
            return rcell

        row_m: int = maze.height - 1
        col_m: int = int(c / 2)

        # Bottom right corner
        if col_m == maze.width:
            rcell.set(type=RCellType.CORNER)
            rcell.set(corner_type=CornerType.BR)
            return rcell

        m_cell: Cell = maze.grid[row_m][col_m]
        if m_cell.west is True:
            rcell.set(corner_type=CornerType.T_UP)
        else:
            rcell.set(corner_type=CornerType.HOR)
        return rcell

    def create(self, maze: "Maze") -> RenderMaze:
        """Generate a RenderMaze from a Maze, filling all RCells.

        Args:
            maze (Maze): The logical maze to render.

        Returns:
            RenderMaze: The fully rendered maze grid.
        """
        render_maze: RenderMaze = RenderMaze(maze)
        r_grid: List[List[RCell]] = render_maze.grid
        a_grid: List[List[Cell]] = maze.grid
        last_row = render_maze.height - 1
        last_col = render_maze.width - 1

        for r, row in enumerate(a_grid):
            # turn 1 Cell into 4 separate RCells
            for c, col in enumerate(row):
                top = self.get_top_cell(r, c, maze)
                prev = self. get_prev_cell(r, c, maze)
                # in Order: top left, top right, center left, center right
                r_grid[r*2][c*2] = self.set_corner(col, top, prev)
                r_grid[r*2][c*2 + 1] = self.set_hor_wall(col, top)
                r_grid[r*2 + 1][c*2] = self.set_ver_wall(col, prev)
                r_grid[r*2 + 1][c*2 + 1] = self.set_center(col)

            # set last corner and vertical wall for each row
            if r == 0:
                r_grid[r*2][last_col].set(type=RCellType.CORNER)
                r_grid[r*2][last_col].set(corner_type=CornerType.TR)
            else:
                r_grid[r*2][last_col] = self.set_last_col_corner(col)
            r_grid[r*2 + 1][last_col].set(type=RCellType.VERTICAL)

        # set last row
        for c in range(render_maze.width):
            r_grid[last_row][c] = self.set_last_row(c, maze)

        return render_maze
