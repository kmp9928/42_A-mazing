from typing import List, Optional
from dataclasses import dataclass
from errors import DirectionError


@dataclass
class Cell:
    west: int = 1
    south: int = 1
    east: int = 1
    north: int = 1
    blocked: bool = False

    def __repr__(self):
        # For printing maze. !!!! Remove before submission !!!!
        b = " "
        if self.blocked:
            b = "X"
        return f"{b}w{self.west}s{self.south}e{self.east}n{self.north}{b}"

    def set(
        self,
        west: Optional[bool] = None,
        south: Optional[bool] = None,
        east: Optional[bool] = None,
        north: Optional[bool] = None,
        blocked: Optional[bool] = None
    ) -> "Cell":
        if west is not None:
            self.west = 1 if west else 0
        if south is not None:
            self.south = 1 if south else 0
        if east is not None:
            self.east = 1 if east else 0
        if north is not None:
            self.north = 1 if north else 0
        if blocked is not None:
            self.blocked = blocked
        return self

    def copy_from(self, cell: "Cell") -> None:
        self.set(
            north=cell.north,
            south=cell.south,
            east=cell.east,
            west=cell.west,
            blocked=cell.blocked
        )


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

    def at(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def carve_at(self, x: int, y: int, direction: str) -> tuple[int, int]:
        """Depending on the direction chosen in the dfs method in the 
        MazeGenerator class, remove the wall between current cell and next
        cell. """
        if direction == "north":
            next_x = x
            next_y = y - 1
            self.at(next_x, next_y).set(south=False)
            self.at(x, y).set(north=False)
        elif direction == "south":
            next_x = x
            next_y = y + 1
            self.at(next_x, next_y).set(north=False)
            self.at(x, y).set(south=False)
        elif direction == "east":
            next_x = x + 1
            next_y = y
            self.at(next_x, next_y).set(west=False)
            self.at(x, y).set(east=False)
        elif direction == "west":
            next_x = x - 1
            next_y = y
            self.at(next_x, next_y).set(east=False)
            self.at(x, y).set(west=False)
        else:
            raise DirectionError(f"Invalid direction {direction} for carving.")

        return (next_x, next_y)

    def get_blocked_cells(self) -> List[tuple[int, int]]:
        return [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.at(x, y).blocked
        ]

    def paste(self, maze: "Maze", offset_x: int, offset_y: int) -> None:
        for x in range(maze.width):
            for y in range(maze.height):
                paste_x = offset_x + x
                paste_y = offset_y + y
                self.at(paste_x, paste_y).copy_from(maze.at(x, y))
