from typing import List
import random
from sys import stderr
from config_parser import Config
from errors import EntryExitInFTError
from maze import CellType, Maze, Coordinate
from maze_42 import maze_42
from gpt_maze_visualizer import print_maze
import datetime


class MazeGenerator:
    visited: List[tuple[int, int]]
    maze: Maze

    def __init__(self, config: Config) -> None:
        self.config = config
        self.visited = []
        self.maze = Maze(0, 0)
        random.seed(1 if self.config.seed is not None else self.config.seed)

    def create(self) -> Maze:
        """Create fully closed maze data structure to start (a grid of class 
        Maze with all the cells closed). Then, add the "42" pattern and the 
        cells from the pattern in "visited" cells. Finally, call dfs method to
        carve out maze."""
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
        print(datetime.datetime.now())
        self.dfs()
        if not self.config.perfect:
            self.make_imperfect()
        print(datetime.datetime.now())
        self.bfs()
        print(datetime.datetime.now())
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

    def dfs(self):
        """"Depth first search. Carves out the maze by opening a wall of the
        cells in the maze by moving to neighboring unvisited cells. Once a dead
        end is reached, the function backtracks."""
        stack = [(self.config.entry, self.config.entry)]
        while stack:
            previous_coordinate, current_coordinate = stack[0]
            del stack[0]
            if current_coordinate in self.visited:
                continue
            self.visited.append(current_coordinate)
            self.maze.set_wall_at(previous_coordinate, current_coordinate, False)
            stack = self.get_unvisited_neighbors(current_coordinate) + stack

    def get_unvisited_neighbors(
            self, coordinate: Coordinate, bottom_and_right_only: bool = False
    ) -> List[tuple[Coordinate, Coordinate]]:
        """Check for a cell which of the cells around it haven't been
        visited in the dfs method."""
        x, y = coordinate
        result: List[tuple[Coordinate, Coordinate]] = []

        if not bottom_and_right_only:
            # north
            if y > 0 and (x, y - 1) not in self.visited:
                result.append(((x, y), (x, y - 1)))

            # west
            if x > 0 and (x - 1, y) not in self.visited:
                result.append(((x, y), (x - 1, y)))

        # south
        if y < self.config.height - 1 and (x, y + 1) not in self.visited:
            result.append(((x, y), (x, y + 1)))

        # east
        if x < self.config.width - 1 and (x + 1, y) not in self.visited:
            result.append(((x, y), (x + 1, y)))

        random.shuffle(result)
        return result

    def make_imperfect(self) -> None:
        self.visited = self.maze.get_blocked_cells()
        for x, y in self.maze.get_all_coordinates():
            if self.maze.get_cell(x, y).blocked:
                continue
            for coordinate in self.get_unvisited_neighbors((x, y), True):
                # get_unvisited_neighbors gets right & bottom neighbors only
                prev_coordinate, curr_coordinate = coordinate
                if (
                    self.check_wall(prev_coordinate, curr_coordinate)
                    and random.random() < 0.1
                ):
                    self.remove_wall_if_valid(prev_coordinate, curr_coordinate)
                    # only one wall broken == less chances of more than 2x3/3x2

    def check_wall(
            self,
            previous_coordinate: Coordinate,
            current_coordinate: Coordinate
    ) -> bool:
        previous_x, previous_y = previous_coordinate
        x, y = current_coordinate

        if x > previous_x:
            return self.maze.get_cell(previous_x, previous_y).east
        elif x < previous_x:
            return self.maze.get_cell(previous_x, previous_y).west
        elif y > previous_y:
            return self.maze.get_cell(previous_x, previous_y).south
        elif y < previous_y:
            return self.maze.get_cell(previous_x, previous_y).north
        else:
            assert False, "Unreachable state, this should not happen."

    def bfs(self) -> None:
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
                    not self.check_wall(prev_coordinate, curr_coordinate)
                    and curr_coordinate not in history
                ):
                    history[curr_coordinate] = prev_coordinate
                    stack.append(curr_coordinate)

        backwards = self.config.exit
        while backwards is not None:
            self.maze.get_cell(*backwards).set(type=CellType.PATH)
            backwards = history.get(backwards)
        self.maze.get_cell(*self.config.entry).set(type=CellType.ENTRY)
        self.maze.get_cell(*self.config.exit).set(type=CellType.EXIT)

    def remove_wall_if_valid(
            self,
            previous_coordinate: Coordinate,
            current_coordinate: Coordinate
    ) -> None:
        x, y = previous_coordinate

        self.maze.set_wall_at(previous_coordinate, current_coordinate, False)

        row = 0
        rectangle = []
        horizontal_size = self.get_horizontal_size(x, y)
        if horizontal_size > 2:
            rectangle.append(horizontal_size)
            top, bottom = self.get_vertical_size(x, y)
            for i in range(1, top + 1):
                row += 1
                size = self.get_horizontal_size(x, y - i)
                rectangle = [size] + rectangle

            for i in range(1, bottom + 1):
                row += 1
                size = self.get_horizontal_size(x, y + i)
                rectangle.append(size)

            if (
                len([val for val in rectangle[:3] if val > 2]) < 3 or
                len([val for val in rectangle[:-3] if val > 2]) < 3 or
                len([val for val in rectangle[1:4] if val > 2]) < 3
            ):
                return

            self.maze.set_wall_at(previous_coordinate, current_coordinate, True)

    def get_horizontal_size(self, x: int, y: int) -> int:
        right = 0
        while x + right < self.config.width - 1 and not self.check_wall((x + right, y), (x + right + 1, y)):
            right += 1

        left = 0
        while x - left > 0 and not self.check_wall((x - left, y), (x - left - 1, y)):
            left += 1

        return right + left + 1

    def get_vertical_size(self, x: int, y: int) -> tuple[int, int]:
        top = 0
        while y - top > 0 and not self.check_wall((x, y - top), (x, y - top - 1)):
            top += 1

        bottom = 0
        while y + bottom < self.config.height - 1 and not self.check_wall((x, y + bottom), (x, y + bottom + 1)):
            bottom += 1

        return (2 if top > 2 else top, 2 if bottom > 2 else bottom)


if __name__ == "__main__":
    print("=== Generate maze ===")
    config = Config(
        width=100,
        height=100,
        entry=(1, 1),
        exit=(79, 49),
        output_file="example.txt",
        perfect=False,
        seed=1
    )
    maze_genertor = MazeGenerator(config)
    maze = maze_genertor.create()
    # for row in maze.grid:
    #     print(row)
    print("FINAL")
    print_maze(maze, config.height, config.width)
