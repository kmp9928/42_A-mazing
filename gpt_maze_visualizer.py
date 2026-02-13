from maze import Maze


def print_maze(maze: Maze, height: int, width: int):

    for y in range(height):
        # --- Draw north walls ---
        top_line = ""
        for x in range(width):
            top_line += "+"
            if maze.at(x, y).north == 1:
                top_line += "---"
            else:
                top_line += "   "
        top_line += "+"
        print(top_line)

        # --- Draw west/east walls ---
        middle_line = ""
        for x in range(width):
            if maze.at(x, y).west == 1:
                middle_line += "|"
            else:
                middle_line += " "

            middle_line += "   "

        # right border (east wall of last cell)
        if maze.at(width - 1, y).east == 1:
            middle_line += "|"
        else:
            middle_line += " "

        print(middle_line)

    # --- Draw bottom border using south walls of last row ---
    bottom_line = ""
    for x in range(width):
        bottom_line += "+"
        if maze.at(x, height - 1).south == 1:
            bottom_line += "---"
        else:
            bottom_line += "   "
    bottom_line += "+"
    print(bottom_line)
