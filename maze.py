from typing import List
from enum import Enum
from dataclasses import dataclass

type Coordinate = tuple[int, int]


class CellType(Enum):
    OPEN = 0
    BLOCKED = 1
    PATH = 2
    ENTRY = 3
    EXIT = 4


@dataclass
class Cell:
    """Cell properties describe walls (or lack of) for a cell in a maze.
    Cell can be of one type:
    - Open
    - Blocked (filled cell)
    - Path (solution for the maze)

    Example usage:
    ```
    cell = Cell(type=CellType.BLOCKED)
    cell.blocked == True
    cell.open == False
    cell.path == False
    cell.north == True
    cell.south == True
    ```
    """
    west: bool = True
    south: bool = True
    east: bool = True
    north: bool = True
    type: CellType = CellType.OPEN

    @property
    def open(self) -> bool:
        return self.type == CellType.OPEN

    @property
    def blocked(self) -> bool:
        return self.type == CellType.BLOCKED

    @property
    def path(self) -> bool:
        return self.type == CellType.PATH

    @property
    def entry(self) -> bool:
        return self.type == CellType.ENTRY

    @property
    def exit(self) -> bool:
        return self.type == CellType.EXIT

    def __repr__(self):
        # !!!! For printing maze. Remove before submission !!!!
        t = "O"
        if self.blocked:
            t = "B"
        elif self.path:
            t = "P"
        elif self.entry:
            t = "e"
        elif self.exit:
            t = "E"
        w = 1 if self.west else 0
        s = 1 if self.south else 0
        e = 1 if self.east else 0
        n = 1 if self.north else 0
        return f"{t}w{w}s{s}e{e}n{n}{t}"

    def set(self, **kwargs) -> "Cell":
        """ Sets the cell properties.
        For example:
        - cell.set(north=True)
        - cell.set(type=CellType.BLOCKED)
        """
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        return self


class Maze:
    grid: List[List[Cell]]
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = []

        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(Cell())
            self.grid.append(row)

    def get_all_coordinates(self) -> List[Coordinate]:
        return [
            (x, y) for x in range(self.height)
            for y in range(self.width)
        ]

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def carve_at(
        self, previous_coordinate: Coordinate, current_coordinate: Coordinate
    ) -> bool:
        """Depending on the direction chosen in the dfs method in the
        MazeGenerator class, remove the wall between current cell and next
        cell. """
        if previous_coordinate == current_coordinate:
            return False

        previous_x, previous_y = previous_coordinate
        x, y = current_coordinate
        if y < previous_y:
            self.get_cell(x, y).set(south=False)
            self.get_cell(previous_x, previous_y).set(north=False)
        elif y > previous_y:
            self.get_cell(x, y).set(north=False)
            self.get_cell(previous_x, previous_y).set(south=False)
        elif x > previous_x:
            self.get_cell(x, y).set(west=False)
            self.get_cell(previous_x, previous_y).set(east=False)
        elif x < previous_x:
            self.get_cell(x, y).set(east=False)
            self.get_cell(previous_x, previous_y).set(west=False)
        else:
            assert False, "Unreachable state, this should not happen."

        return True

    def get_blocked_cells(self) -> List[tuple[int, int]]:
        return [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.get_cell(x, y).blocked
        ]

    def copy_from(self, source: "Maze", offset_x: int, offset_y: int) -> None:
        for x in range(source.width):
            for y in range(source.height):
                paste_x = offset_x + x
                paste_y = offset_y + y
                # Copy cell values from source maze to current maze
                self.get_cell(paste_x, paste_y).set(
                    **source.get_cell(x, y).__dict__
                )
