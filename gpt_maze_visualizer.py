from maze import Maze


def print_maze(maze: Maze, height: int, width: int):

    for y in range(height):
        # --- Draw north walls ---
        top_line = ""
        for x in range(width):
            top_line += "+"
            if maze.get_cell(x, y).north == 1:
                top_line += "---"
            else:
                top_line += "   "
        top_line += "+"
        print(top_line)

        # --- Draw west/east walls ---
        middle_line = ""
        for x in range(width):
            if maze.get_cell(x, y).west == 1:
                middle_line += "|"
            else:
                middle_line += " "
            
            symbol = '   '
            if maze.get_cell(x, y).blocked:
                symbol = 'XXX'
            elif maze.get_cell(x, y).path:
                symbol = ' P '
            elif maze.get_cell(x, y).entry:
                symbol = '<e>'
            elif maze.get_cell(x, y).exit:
                symbol = '[E]'
            
            middle_line += symbol

        # right border (east wall of last cell)
        if maze.get_cell(width - 1, y).east == 1:
            middle_line += "|"
        else:
            middle_line += " "

        print(middle_line)

    # --- Draw bottom border using south walls of last row ---
    bottom_line = ""
    for x in range(width):
        bottom_line += "+"
        if maze.get_cell(x, height - 1).south == 1:
            bottom_line += "---"
        else:
            bottom_line += "   "
    bottom_line += "+"
    print(bottom_line)
