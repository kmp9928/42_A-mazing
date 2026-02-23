*This project has been created as part of the 42 curriculum by sukerl, kimendon.*


## MazeGenerator

`MazeGenerator` generates and solves mazes using:

- Depth-First Search (DFS) for maze carving.
- Optional wall removal for imperfect mazes.
- Breadth-First Search (BFS) for shortest-path solving.

The generator creates a fully closed maze, optionally embeds a fixed "42" pattern (if size permits), carves passages, and computes the shortest path from entry to exit.


## Basic Usage

```python
from maze.generator import MazeGenerator
from maze.config import Config

config = Config(
    width=15,
    height=15,
    entry=(0, 0),
    exit=(14, 14),
    seed=1,
    perfect=True
)

generator = MazeGenerator(config)
maze = generator.create_maze()
```

This will create a perfect maze of 15 x 15 with the "42" pattern and the shortest solution path. 


## Configuration Options

The `Config` object controls the maze generation:

| Parameter | Type          | Description                       |
| --------- | ------------- | --------------------------------- |
| `width`   | `int`         | Maze width                        |
| `height`  | `int`         | Maze height                       |
| `entry`   | `(x, y)`      | Entry coordinate                  |
| `exit`    | `(x, y)`      | Exit coordinate                   |
| `perfect` | `bool`        | If `True`, maze has only 1 solution and no loops      |
| `seed`    | `int \| None` | Random seed (for reproducibility) |

Note: The initial project for which this module was created asked for the parameter `output_file` in `Config`. This field can be removed from it for future usages.

## Accessing the Maze Structure

After the maze is created:
```python
maze.width
maze.height
```


## Accessing the Solution Path

To get the solution path coordinates:

```python
path = maze.get_path()
print(path)

#Example output:
[(0, 0), (1, 0), (1, 1), ..., (14, 14)]
```


## Complete Example

```python
config = Config(
    width=10,
    height=10,
    entry=(0, 0),
    exit=(9, 9),
    seed=42,
    perfect=False
)

generator = MazeGenerator(config)
maze = generator.create_maze()

print("Maze size:", maze.width, "x", maze.height)
print("Solution length:", len(maze.get_path()))
print("Solution path:", maze.get_path())
```
