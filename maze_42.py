from maze import Maze, CellType

maze_42 = Maze(7, 5)

# 4
maze_42.get_cell(0, 0).set(type=CellType.BLOCKED)
maze_42.get_cell(0, 1).set(type=CellType.BLOCKED)
maze_42.get_cell(0, 2).set(type=CellType.BLOCKED)
maze_42.get_cell(1, 2).set(type=CellType.BLOCKED)
maze_42.get_cell(2, 0).set(type=CellType.BLOCKED)
maze_42.get_cell(2, 1).set(type=CellType.BLOCKED)
maze_42.get_cell(2, 2).set(type=CellType.BLOCKED)
maze_42.get_cell(2, 3).set(type=CellType.BLOCKED)
maze_42.get_cell(2, 4).set(type=CellType.BLOCKED)

# 2
maze_42.get_cell(4, 0).set(type=CellType.BLOCKED)
maze_42.get_cell(5, 0).set(type=CellType.BLOCKED)
maze_42.get_cell(6, 0).set(type=CellType.BLOCKED)
maze_42.get_cell(6, 1).set(type=CellType.BLOCKED)
maze_42.get_cell(6, 2).set(type=CellType.BLOCKED)
maze_42.get_cell(5, 2).set(type=CellType.BLOCKED)
maze_42.get_cell(4, 2).set(type=CellType.BLOCKED)
maze_42.get_cell(4, 3).set(type=CellType.BLOCKED)
maze_42.get_cell(4, 4).set(type=CellType.BLOCKED)
maze_42.get_cell(5, 4).set(type=CellType.BLOCKED)
maze_42.get_cell(6, 4).set(type=CellType.BLOCKED)
