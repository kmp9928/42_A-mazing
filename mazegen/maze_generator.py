from typing import List
import random
from sys import stderr
from .config_parser import Config
from .errors import EntryExitInFTError
from .maze import CellType, Maze, Coordinate
from .maze_42 import maze_42
# import datetime


class MazeGenerator:
    """Generate a maze based on a configuration and solve it.

    The generator creates a fully closed maze. Depending on the size, it embeds
    a fixed "42" pattern. The generator carves the walls using depth-first
    search (DFS) algorithm and, optionally, removes additional walls to make
    the maze imperfect. Finally, it computes a path from entry to exit using
    breadth-first search (BFS) algorithm.

    Attributes:
        visited (List[Coordinate]): Coordinates visited at certain point.
        maze (Maze): The maze data structure being generated.
        config (Config): Configuration object controlling generation.
    """
    visited: List[Coordinate]
    maze: Maze

    def __init__(self, config: Config) -> None:
        """Initialize the maze generator.

        Args:
            config (Config): Configuration data containing (at least) maze
                dimensions, entry/exit coordinates and generation options.

        Example:
            >>> generator = MazeGenerator(config)
            >>> maze = generator.create_maze()
        """
        self.config = config
        self.visited = []
        self.maze = Maze(0, 0)
        random.seed(1 if self.config.seed is None else self.config.seed)

    def create_maze(self) -> Maze:
        """Generate a complete maze.

        First fully closed maze grid is created. Then, the "42" pattern is
        added in the center, if possible. The passages are carved and
        additional walls get removed, if the maze is imperfect. Finally, the
        shortest solution path is determined.

        Returns:
            Maze: The generated maze instance.

        Raises:
            EntryExitInFTError: If the configured entry or exit coordinates are
                inside the fixed "42" pattern.
        """
        self.maze = Maze(self.config.width, self.config.height)
        self.draw_42()
        self.visited = self.maze.get_blocked_cells()
        if (
            self.config.entry in self.visited or
            self.config.exit in self.visited
        ):
            raise EntryExitInFTError(
                "Entry/exit points in '42' pattern. For this maze, points "
                f"can't be any of these coordinates: {self.visited}"
            )
        # print(datetime.datetime.now())
        self.carve_maze()
        if not self.config.perfect:
            self.make_imperfect()
        # print(datetime.datetime.now())
        self.solve_maze()
        # print(datetime.datetime.now())
        return self.maze

    def draw_42(self) -> None:
        """Embed the "42" pattern into the maze.

        If the maze size allows, the pattern is copied from a predefined
        mini-maze and placed in the center of the current maze grid. Otherwise,
        the method exists without modifying the maze.
        """
        if (
            self.maze.width < maze_42.width + 2 or
            self.maze.height < maze_42.height + 2
        ):
            print("Maze size doesn't allow drawing '42' pattern.", file=stderr)
            return
        x = int((self.maze.width - maze_42.width) / 2)
        y = int((self.maze.height - maze_42.height) / 2)
        self.maze.copy_from(maze_42, x, y)

    def carve_maze(self):
        """Carve the maze using depth-first search (DFS) algorithm.

        Starting from the entry point, the algorithm visits
        neighboring unvisited cells and removes walls between them.
        When reaching a dead end, it backtracks using a stack-based
        approach until all reachable cells are visited.
        """
        stack: List[tuple[Coordinate, Coordinate]] = [
            (self.config.entry, self.config.entry)
        ]

        while stack:
            previous_coordinate, current_coordinate = stack[0]
            del stack[0]
            if current_coordinate in self.visited:
                continue
            self.visited.append(current_coordinate)
            self.maze.set_wall_at(
                previous_coordinate, current_coordinate, False
            )
            stack = self.get_unvisited_neighbors(current_coordinate) + stack

    def get_unvisited_neighbors(
            self, coordinate: Coordinate, bottom_and_right_only: bool = False
    ) -> List[tuple[Coordinate, Coordinate]]:
        """Return unvisited neighboring cells.

        Args:
            coordinate (Coordinate): The current cell (x, y).
            bottom_and_right_only (bool, optional): If True, only
                considers south and east neighbors. Defaults to False.

        Returns:
            List[tuple[Coordinate, Coordinate]]: A list of
                (current_cell, neighbor_cell) pairs representing
                valid unvisited neighbors.
        """
        x, y = coordinate
        result: List[tuple[Coordinate, Coordinate]] = []

        if not bottom_and_right_only:
            if y > 0 and (x, y - 1) not in self.visited:
                result.append(((x, y), (x, y - 1)))

            if x > 0 and (x - 1, y) not in self.visited:
                result.append(((x, y), (x - 1, y)))

        if y < self.config.height - 1 and (x, y + 1) not in self.visited:
            result.append(((x, y), (x, y + 1)))

        if x < self.config.width - 1 and (x + 1, y) not in self.visited:
            result.append(((x, y), (x + 1, y)))

        random.shuffle(result)
        return result

    def make_imperfect(self) -> None:
        """Remove additional walls to make the maze imperfect.

        Iterates over all cells and randomly removes walls between
        adjacent cells (right and bottom only) with a fixed probability of 10%,
        making sure that doing so does not create invalid 2x3 or 3x2 open
        regions.
        """
        self.visited = self.maze.get_blocked_cells()

        for x, y in self.maze.get_all_coordinates():
            if self.maze.get_cell(x, y).blocked:
                continue
            for coordinate in self.get_unvisited_neighbors((x, y), True):
                prev_coordinate, curr_coordinate = coordinate
                if (
                    self.maze.has_wall_between(
                        prev_coordinate, curr_coordinate
                    )
                    and random.random() < 0.1
                ):
                    self.remove_wall_if_valid(prev_coordinate, curr_coordinate)

    def solve_maze(self) -> None:
        """Find and save the shortest path from entry to exit.

        Performs breadth-first search (BFS) to compute the shortest
        path from the configured entry to the exit. The resulting path
        is stored.
        """
        self.visited = self.maze.get_blocked_cells()
        stack = [self.config.entry]
        history = {self.config.entry: None}

        while stack:
            prev_coordinate = stack[0]
            del stack[0]
            if prev_coordinate == self.config.exit:
                break
            for coordinate in self.get_unvisited_neighbors(prev_coordinate):
                prev_coordinate, curr_coordinate = coordinate
                if (
                    not self.maze.has_wall_between(
                        prev_coordinate, curr_coordinate
                    )
                    and curr_coordinate not in history
                ):
                    history[curr_coordinate] = prev_coordinate
                    stack.append(curr_coordinate)

        path: List[Coordinate] = []
        coordinate = self.config.exit
        while coordinate is not None:
            self.maze.get_cell(*coordinate).set(type=CellType.PATH)
            path.append(coordinate)
            coordinate = history.get(coordinate)

        path.reverse()
        self.maze.set_path(path)
        self.maze.get_cell(*self.config.entry).set(type=CellType.ENTRY)
        self.maze.get_cell(*self.config.exit).set(type=CellType.EXIT)

    def remove_wall_if_valid(
            self, prev_coordinate: Coordinate, curr_coordinate: Coordinate
    ) -> None:
        """Remove a wall if by doing it no invalid square regions are created.

        Temporarily removes the wall between two adjacent cells and checks
        whether this creates a fully open 3x3 region. If such a region is
        detected, the wall is restored.

        Args:
            prev_coordinate (Coordinate): First cell.
            curr_coordinate (Coordinate): Adjacent cell.
        """
        self.maze.set_wall_at(prev_coordinate, curr_coordinate, False)

        for square in self.get_invalid_size_squares(
            (prev_coordinate, curr_coordinate)
        ):
            inner_walls = 0
            for x in range(0, 7, 3):
                for y in range(2):
                    if self.maze.has_wall_between(
                        square[x + y], square[x + y + 1]
                    ):
                        inner_walls += 1
                if x < 6:
                    for y in range(3):
                        if self.maze.has_wall_between(
                            square[y], square[y + 3]
                        ):
                            inner_walls += 1

            if inner_walls == 0:
                self.maze.set_wall_at(prev_coordinate, curr_coordinate, True)
                break

    def get_invalid_size_squares(
            self, adj_cells: tuple[Coordinate, Coordinate]
    ) -> List[List[Coordinate]]:
        """Return all 3x3 squares that include the given adjacent cells.

        Computes every possible 3x3 region in the maze that contains
        both provided adjacent cells.

        Args:
            adj_cells (tuple[Coordinate, Coordinate]): Two adjacent cells.

        Returns:
            List[List[Coordinate]]: A list of 3x3 squares, where each square
                is represented as a list of nine coordinates.
        """
        min_x = max(max(0, row - 3 - 1) for row, _ in adj_cells)
        max_x = min(min(self.config.width - 3, row) for row, _ in adj_cells)

        min_y = max(max(0, col - 3 - 1) for _, col in adj_cells)
        max_y = min(min(self.config.height - 3, col) for _, col in adj_cells)

        invalid_size_squares: List[List[Coordinate]] = []
        for row in range(min_x, max_x + 1):
            for col in range(min_y, max_y + 1):
                square = [
                    (x, y)
                    for x in range(row, row + 3)
                    for y in range(col, col + 3)
                ]
                invalid_size_squares.append(square)

        return invalid_size_squares
