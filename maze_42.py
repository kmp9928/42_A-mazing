from maze import Maze

maze_42 = Maze(7, 7)

# 4
maze_42.at(0, 0).set(blocked=True)
maze_42.at(0, 1).set(blocked=True)
maze_42.at(0, 2).set(blocked=True)
maze_42.at(1, 2).set(blocked=True)
maze_42.at(2, 2).set(blocked=True)
maze_42.at(2, 3).set(blocked=True)
maze_42.at(2, 4).set(blocked=True)

# 2
maze_42.at(4, 0).set(blocked=True)
maze_42.at(5, 0).set(blocked=True)
maze_42.at(6, 0).set(blocked=True)
maze_42.at(6, 1).set(blocked=True)
maze_42.at(6, 2).set(blocked=True)
maze_42.at(5, 2).set(blocked=True)
maze_42.at(4, 2).set(blocked=True)
maze_42.at(4, 3).set(blocked=True)
maze_42.at(4, 4).set(blocked=True)
maze_42.at(5, 4).set(blocked=True)
maze_42.at(6, 4).set(blocked=True)
