from typing import List, Union
from enum import Enum
from dataclasses import dataclass

type Coordinate = tuple[int, int]


class CellType(Enum):
    """Possible cell types in a maze.

    Attributes:
        OPEN: A walkable cell.
        BLOCKED: A cell fully closed for the "42" pattern.
        PATH: A cell that is part of the solved path.
        ENTRY: The maze entry point.
        EXIT: The maze exit point.
    """
    OPEN = 0
    BLOCKED = 1
    PATH = 2
    ENTRY = 3
    EXIT = 4


@dataclass
class Cell:
    """Represent a single maze cell.

    A cell contains four walls (north, south, east, west) and a type
    describing its role in the maze (open, blocked, path, entry, exit).

    By default, all walls are present and the cell is open.

    Attributes:
        west (bool): Whether a west wall exists.
        south (bool): Whether a south wall exists.
        east (bool): Whether an east wall exists.
        north (bool): Whether a north wall exists.
        type (CellType): The type of the cell.
    """
    west: bool = True
    south: bool = True
    east: bool = True
    north: bool = True
    type: CellType = CellType.OPEN

    @property
    def open(self) -> bool:
        """Return True if the cell is open."""
        return self.type == CellType.OPEN

    @property
    def blocked(self) -> bool:
        """Return True if the cell is blocked."""
        return self.type == CellType.BLOCKED

    @property
    def path(self) -> bool:
        """Return True if the cell is part of the solution path."""
        return self.type == CellType.PATH

    @property
    def entry(self) -> bool:
        """Return True if the cell is the entry of the maze."""
        return self.type == CellType.ENTRY

    @property
    def exit(self) -> bool:
        """Return True if the cell is the exit of the maze."""
        return self.type == CellType.EXIT

    def set(self, **kwargs: Union[bool, CellType]) -> "Cell":
        """Update one or more cell attributes.

        Args:
            **kwargs (Union[bool, CellType]): Attribute-value pairs to update.

        Returns:
            Cell: The updated cell instance (allows method chaining).

        Example:
            >>> cell.set(north=False)
            >>> cell.set(type=CellType.BLOCKED)
        """
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        return self


class Maze:
    """Represent a 2D maze grid composed of Cell objects.

    The maze maintains a grid of cells, supports wall manipulation
    between adjacent cells and stores the solution path.

    Attributes:
        grid (List[List[Cell]]): 2D grid of cells indexed as [y][x].
        width (int): Number of columns in the maze.
        height (int): Number of rows in the maze.
        path (List[Coordinate]): Solution path from entry to exit.
    """
    grid: List[List[Cell]]
    width: int
    height: int
    path: List[Coordinate]

    def __init__(self, width: int, height: int) -> None:
        """Initialize a maze with given dimensions.

        All cells are initialized as open with all four walls present.

        Args:
            width (int): Number of columns.
            height (int): Number of rows.
        """
        self.width = width
        self.height = height
        self.grid = []
        self.path = []

        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(Cell())
            self.grid.append(row)

    def get_all_coordinates(self) -> List[Coordinate]:
        """Return all coordinates in the maze.

        Returns:
            List[Coordinate]: List of (x, y) coordinates.
        """
        return [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell at the given coordinates.

        Args:
            x (int): Column index.
            y (int): Row index.

        Returns:
            Cell: The corresponding cell instance.
        """

        return self.grid[y][x]

    def get_blocked_cells(self) -> List[Coordinate]:
        """Return coordinates of all blocked cells.

        Returns:
            List[Coordinate]: List of (x, y) coordinates
                where the cell type is BLOCKED.
        """
        return [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.get_cell(x, y).blocked
        ]

    def has_wall_between(
            self,
            previous_coordinate: Coordinate,
            current_coordinate: Coordinate
    ) -> bool:
        """Check whether a wall exists between two adjacent cells.

        Args:
            previous_coordinate (Coordinate): First cell.
            current_coordinate (Coordinate): Adjacent cell.

        Returns:
            bool: True if a wall exists between the cells.
        """
        previous_x, previous_y = previous_coordinate
        x, y = current_coordinate

        if x > previous_x:
            return self.get_cell(previous_x, previous_y).east
        elif x < previous_x:
            return self.get_cell(previous_x, previous_y).west
        elif y > previous_y:
            return self.get_cell(previous_x, previous_y).south
        elif y < previous_y:
            return self.get_cell(previous_x, previous_y).north

        assert False, "This should't happen"

    def set_wall_at(
        self,
        previous_coordinate: Coordinate,
        current_coordinate: Coordinate,
        set_wall: bool
    ) -> bool:
        """Add or remove the wall between two adjacent cells.

        Updates both cells symmetrically to maintain consistency.

        Args:
            previous_coordinate (Coordinate): First cell.
            current_coordinate (Coordinate): Adjacent cell.
            set_wall (bool): True to add a wall, False to remove it.

        Returns:
            bool: False if coordinates are identical,
                True otherwise.
        """
        if previous_coordinate == current_coordinate:
            return False

        previous_x, previous_y = previous_coordinate
        x, y = current_coordinate
        if y < previous_y:
            self.get_cell(x, y).set(south=set_wall)
            self.get_cell(previous_x, previous_y).set(north=set_wall)
        elif y > previous_y:
            self.get_cell(x, y).set(north=set_wall)
            self.get_cell(previous_x, previous_y).set(south=set_wall)
        elif x > previous_x:
            self.get_cell(x, y).set(west=set_wall)
            self.get_cell(previous_x, previous_y).set(east=set_wall)
        elif x < previous_x:
            self.get_cell(x, y).set(east=set_wall)
            self.get_cell(previous_x, previous_y).set(west=set_wall)

        return True

    def copy_from(self, source: "Maze", offset_x: int, offset_y: int) -> None:
        """Copy cell data from source maze.

        Cells from the source maze are copied starting at the specified offset.

        Args:
            source (Maze): The maze to copy from.
            offset_x (int): Horizontal offset in target maze.
            offset_y (int): Vertical offset in target maze.
        """
        for x in range(source.width):
            for y in range(source.height):
                paste_x = offset_x + x
                paste_y = offset_y + y
                self.get_cell(paste_x, paste_y).set(
                    **source.get_cell(x, y).__dict__
                )

    def set_path(self, path: List[Coordinate]) -> None:
        """Store the solution path.

        Args:
            path (List[Coordinate]): Ordered list of path coordinates.
        """
        self.path = path

    def get_path(self) -> List[Coordinate]:
        """Return the stored solution path.

        Returns:
            List[Coordinate]: Ordered path from entry to exit.
        """
        return self.path
