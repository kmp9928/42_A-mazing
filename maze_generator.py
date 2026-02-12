from typing import List
import random
from dataclasses import dataclass
from config_parser import Config


@dataclass
class Cell:
    west: int = 1
    south: int = 1
    east: int = 1
    north: int = 1


@dataclass
class Maze:
    maze: List[List[Cell]]


class MazeGenerator:
    visited: List[tuple[int, int]]
    result: Maze

    def __init__(self, config: Config, seed: int) -> None:
        self.config = config
        self.visited = [(1, 1)]
        self.result = Maze([])
        random.seed(seed)

    def create_maze(self) -> Maze:
        """Create fully closed maze data structure to start (a grid
        of class Maze with all the cells closed). Then call dfs method
        to carve out maze."""
        for _ in range(config.height):
            row = []
            for _ in range(config.width):
                row.append(Cell())
            self.result.maze.append(row)
        self.dfs(1, 1)
        return self.result

    def dfs(self, x: int, y: int):
        """"Depth first search. Carves out the maze by opening a wall of the
        cells in the maze by recursively moving to neighboring unvisited cells.
        Once a dead end is reached, the function backtracks."""
        while True:
            unvisited_neighbors = []

            if y > 0 and (x, y - 1) not in self.visited:
                unvisited_neighbors.append("north")

            if y < config.height - 1 and (x, y + 1) not in self.visited:
                unvisited_neighbors.append("south")

            if x < config.width - 1 and (x + 1, y) not in self.visited:
                unvisited_neighbors.append("east")

            if x > 0 and (x - 1, y) not in self.visited:
                unvisited_neighbors.append("west")

            if len(unvisited_neighbors) == 0:
                return
            else:
                next_cell = random.choice(unvisited_neighbors)

            if next_cell == "north":
                next_x = x
                next_y = y - 1
                self.result.maze[next_y][next_x].south = 0
                self.result.maze[y][x].north = 0
            elif next_cell == "south":
                next_x = x
                next_y = y + 1
                self.result.maze[next_y][next_x].north = 0
                self.result.maze[y][x].south = 0
            elif next_cell == "east":
                next_x = x + 1
                next_y = y
                self.result.maze[next_y][next_x].west = 0
                self.result.maze[y][x].east = 0
            elif next_cell == "west":
                next_x = x - 1
                next_y = y
                self.result.maze[next_y][next_x].east = 0
                self.result.maze[y][x].west = 0

            self.visited.append((next_x, next_y))
            self.dfs(next_x, next_y)


if __name__ == "__main__":
    print("=== Generate maze ===")
    config = Config(
        width=20,
        height=15,
        entry=(1, 1),
        exit=(19, 14),
        output_file="example.txt",
        perfect=True
    )
    seed = 1
    maze = MazeGenerator(config, seed).create_maze()
    print("FINAL")
    for row in maze.maze:
        print(row)
