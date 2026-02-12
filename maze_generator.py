from typing import List
import random
from config_parser import Config
from maze import Maze
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
        # Check min size to add 42 and add error message +++
        if self.maze.width > 10 and self.maze.height > 10:
            self.draw_42()
        self.visited = self.maze.get_blocked_cells()
        self.dfs(0, 0)
        return self.maze

    def draw_42(self) -> None:
        """Draw in the initial grid the "42" pattern. The "drawing" of the 
        pattern is done by a "maze" copy, from a mini "maze" (maze_42) to the
        middle part of the initial grid."""
        # Check min size to add 42 and add error message +++
        x = int((self.maze.width - maze_42.width) / 2)
        y = int((self.maze.height - maze_42.height) / 2)
        self.maze.paste(maze_42, x, y)

    def dfs(self, x: int, y: int):
        """"Depth first search. Carves out the maze by opening a wall of the
        cells in the maze by recursively moving to neighboring unvisited cells.
        Once a dead end is reached, the function backtracks."""
        self.visited.append((x, y))
        while True:
            unvisited_neighbors = self.get_unvisited_neighbors(x, y)

            if len(unvisited_neighbors) == 0:
                return
            else:
                next_cell = random.choice(unvisited_neighbors)

            next_x, next_y = self.maze.carve_at(x, y, next_cell)
            self.dfs(next_x, next_y)

    def get_unvisited_neighbors(self, x: int, y: int) -> List[str]:
        """Check for a cell which of the neighbourhoring cells haven't been 
        visited in the dfs method."""
        result = []

        if y > 0 and (x, y - 1) not in self.visited:
            result.append("north")

        if y < config.height - 1 and (x, y + 1) not in self.visited:
            result.append("south")

        if x < config.width - 1 and (x + 1, y) not in self.visited:
            result.append("east")

        if x > 0 and (x - 1, y) not in self.visited:
            result.append("west")

        return result


if __name__ == "__main__":
    print("=== Generate maze ===")
    config = Config(
        width=15,
        height=20,
        entry=(1, 1),
        exit=(14, 19),
        output_file="example.txt",
        perfect=True
    )
    seed = 1
    maze_genertor = MazeGenerator(config, seed)
    maze = maze_genertor.create()
    print("FINAL")
    print_maze(maze, config.height, config.width)
