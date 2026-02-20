from gpt_maze_visualizer import print_maze
from mazegen import Maze, MazeGenerator, Config

config = Config(
    width=6,
    height=5,
    entry=(0, 0),
    exit=(1, 1),
    output_file="output_maze.txt",
    perfect=True
)
maze_gen = MazeGenerator(config)

maze = Maze(6, 5)

# for coordinate in maze.get_all_coordinates():
#     maze.get_cell(*coordinate).set(north=False, east=False, south=False, west=False)

maze.get_cell(0, 0).set(east=False)
maze.get_cell(0, 0).set(south=False)
maze.get_cell(0, 1).set(north=False)
# maze.get_cell(0, 1).set(south=False)
# maze.get_cell(0, 2).set(north=False)
maze.get_cell(0, 2).set(east=False)
maze.get_cell(1, 0).set(west=False)
maze.get_cell(1, 0).set(south=False)
maze.get_cell(1, 0).set(east=False)
maze.get_cell(2, 0).set(south=False)
maze.get_cell(2, 0).set(west=False)
maze.get_cell(1, 1).set(east=False)
maze.get_cell(1, 1).set(north=False)
maze.get_cell(1, 1).set(south=False)
maze.get_cell(2, 1).set(south=False)
maze.get_cell(2, 1).set(north=False)
maze.get_cell(2, 1).set(west=False)
maze.get_cell(1, 2).set(east=False)
maze.get_cell(1, 2).set(north=False)
maze.get_cell(1, 2).set(west=False)
maze.get_cell(2, 2).set(north=False)
maze.get_cell(2, 2).set(west=False)

# maze.get_cell(1, 1).set(east=True)
# maze.get_cell(2, 1).set(west=True)

maze_gen.maze = maze
print_maze(maze, 5, 6)
print()
maze_gen.remove_wall_if_valid((0, 1), (1, 1))
# maze_gen.remove_wall_if_valid((1, 1), (2, 1))
print_maze(maze, 5, 6)



