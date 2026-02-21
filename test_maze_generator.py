import pytest
from mazegen import Maze, MazeGenerator, MazeGeneratorError, Config, Cell
# from gpt_maze_visualizer import print_maze


def create_maze_gen_and_grid(config: Config) -> MazeGenerator:
    maze_gen = MazeGenerator(config)
    maze_gen.maze = Maze(config.width, config.height)
    return maze_gen


@pytest.mark.parametrize("config,expected_error", [
    (Config(width=10, height=10, entry=(0, 0), exit=(1, 2), output_file='maze.txt', perfect=True), "Entry/exit in '42' pattern. For this maze, entry/exit points can't be any of these coordinates: [(1, 2), (3, 2), (5, 2), (6, 2), (7, 2), (1, 3), (3, 3), (7, 3), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4), (3, 5), (5, 5), (3, 6), (5, 6), (6, 6), (7, 6)]"),
    (Config(width=10, height=10, entry=(6, 6), exit=(9, 9), output_file='maze.txt', perfect=True), "Entry/exit in '42' pattern. For this maze, entry/exit points can't be any of these coordinates: [(1, 2), (3, 2), (5, 2), (6, 2), (7, 2), (1, 3), (3, 3), (7, 3), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4), (3, 5), (5, 5), (3, 6), (5, 6), (6, 6), (7, 6)]")
])
def test_entry_exit_in_ft(config, expected_error):
    with pytest.raises(MazeGeneratorError) as e:
        create_maze_gen_and_grid(config).create_maze()
    assert str(e.value) == expected_error


def test_unvisited_neighbors():
    maze_gen = create_maze_gen_and_grid(Config(width=5, height=5, entry=(0, 0), exit=(4, 4), output_file='maze.txt', perfect=True))
    assert sorted(maze_gen.get_unvisited_neighbors((1, 1))) == sorted([((1, 1), (0, 1)), ((1, 1), (2, 1)), ((1, 1), (1, 0)), ((1, 1), (1, 2))])
    assert sorted(maze_gen.get_unvisited_neighbors((1, 1), True)) == sorted([((1, 1), (2, 1)), ((1, 1), (1, 2))])
    maze_gen.visited = [(1, 0)]
    assert sorted(maze_gen.get_unvisited_neighbors((1, 1))) == sorted([((1, 1), (0, 1)), ((1, 1), (2, 1)), ((1, 1), (1, 2))])


def test_remove_wall_if_valid():
    maze_gen = create_maze_gen_and_grid(Config(width=5, height=5, entry=(0, 0), exit=(4, 4), output_file='maze.txt', perfect=True))
    maze_gen.maze.get_cell(0, 0).set(east=False, south=False)
    maze_gen.maze.get_cell(1, 0).set(east=False, west=False, south=False)
    maze_gen.maze.get_cell(2, 0).set(west=False, south=False)
    maze_gen.maze.get_cell(0, 1).set(north=False, south=False)
    maze_gen.maze.get_cell(1, 1).set(north=False, east=False, south=False)
    maze_gen.maze.get_cell(2, 1).set(north=False, south=False, west=False)
    maze_gen.maze.get_cell(0, 2).set(north=False, east=False)
    maze_gen.maze.get_cell(1, 2).set(north=False, east=False, west=False)
    maze_gen.maze.get_cell(2, 2).set(north=False, west=False)
    # print_maze(maze_gen.maze, 5, 5)
    maze_gen.remove_wall_if_valid((0, 1), (1, 1))
    # print_maze(maze_gen.maze, 5, 5)
    assert maze_gen.maze.get_cell(0, 1) == Cell(north=False, east=True, south=False, west=True)
    assert maze_gen.maze.get_cell(1, 1) == Cell(north=False, east=False, south=False, west=True)
    maze_gen.maze.get_cell(1, 0).set(south=True)
    maze_gen.maze.get_cell(1, 1).set(north=True)
    # print_maze(maze_gen.maze, 5, 5)
    maze_gen.remove_wall_if_valid((1, 0), (1, 1))
    # print_maze(maze_gen.maze, 5, 5)
    assert maze_gen.maze.get_cell(1, 0) == Cell(north=True, east=False, south=False, west=False)
    assert maze_gen.maze.get_cell(1, 1) == Cell(north=False, east=False, south=False, west=True)
    # assert False


def test_get_invalid_size_squares():
    maze_gen = create_maze_gen_and_grid(Config(width=5, height=5, entry=(0, 0), exit=(4, 4), output_file='maze.txt', perfect=True))
    assert maze_gen.get_invalid_size_squares(((0, 1), (1, 1))) == [[(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)], [(0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (0, 3), (1, 3), (2, 3)]]
