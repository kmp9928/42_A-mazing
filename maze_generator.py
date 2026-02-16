from typing import List
import random
from sys import stderr
from config_parser import Config
from errors import EntryExitInFTError
from maze import Maze, Coordinate
from maze_42 import maze_42
from gpt_maze_visualizer import print_maze


class MazeGenerator:
    visited: List[tuple[int, int]]
    maze: Maze

    def __init__(self, config: Config, seed: int) -> None:
        self.config = config
        self.visited = []
        self.maze = Maze(0, 0)
        random.seed(seed)

    def create(self) -> Maze:
        """Create fully closed maze data structure to start (a grid of class 
        Maze with all the cells closed). Then, add the "42" pattern and the 
        cells from the pattern in "visited" cells. Finally, call dfs method to
        carve out maze."""
        self.maze = Maze(config.width, config.height)
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
        self.dfs(self.config.entry)
        return self.maze

    def draw_42(self) -> None:
        """Draw in the initial grid the "42" pattern. The "drawing" of the 
        pattern is done by a "maze" copy, from a mini "maze" (maze_42) to the
        middle part of the initial grid."""
        if (
            self.maze.width < maze_42.width + 2 or
            self.maze.height < maze_42.height + 2
        ):
            print("Maze size doesn't allow drawing '42' pattern.", file=stderr)
            return
        x = int((self.maze.width - maze_42.width) / 2)
        y = int((self.maze.height - maze_42.height) / 2)
        self.maze.copy_from(maze_42, x, y)

    def dfs(self, coordinate: Coordinate):
        """"Depth first search. Carves out the maze by opening a wall of the
        cells in the maze by recursively moving to neighboring unvisited cells.
        Once a dead end is reached, the function backtracks."""
        stack = [(coordinate, coordinate)]
        while stack:
            previous_coordinate, current_coordinate = stack[0]
            del stack[0]
            if current_coordinate in self.visited:
                continue
            self.visited.append(current_coordinate)
            self.maze.carve_at(previous_coordinate, current_coordinate)
            stack = self.get_unvisited_neighbors(current_coordinate) + stack

    def get_unvisited_neighbors(
            self, coordinate: Coordinate
    ) -> List[tuple[Coordinate, Coordinate]]:
        """Check for a cell which of the cells around it haven't been
        visited in the dfs method."""
        x, y = coordinate
        result: List[tuple[Coordinate, Coordinate]] = []

        if y > 0 and (x, y - 1) not in self.visited:
            result.append(((x, y), (x, y - 1)))

        if y < config.height - 1 and (x, y + 1) not in self.visited:
            result.append(((x, y), (x, y + 1)))

        if x < config.width - 1 and (x + 1, y) not in self.visited:
            result.append(((x, y), (x + 1, y)))

        if x > 0 and (x - 1, y) not in self.visited:
            result.append(((x, y), (x - 1, y)))

        random.shuffle(result)
        return result


if __name__ == "__main__":
    print("=== Generate maze ===")
    config = Config(
        width=20,
        height=20,
        entry=(1, 1),
        exit=(1, 2),
        output_file="example.txt",
        perfect=True
    )
    seed = 1
    maze_genertor = MazeGenerator(config, seed)
    maze = maze_genertor.create()
    for row in maze.grid:
        print(row)
    print("FINAL")
    print_maze(maze, config.height, config.width)
