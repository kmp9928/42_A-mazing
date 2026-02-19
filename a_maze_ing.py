#!/usr/bin/env python3

from mazegen import MazeGenerator, Config
from print_ascii import AsciiPrinter
# from sukerl_print_ascii import XAsciiPrinter
from create_output_txt import OutputGenerator
# from gpt_maze_visualizer import print_maze

if __name__ == "__main__":
    print("=== Generate maze ===")
    config = Config(
        width=12,
        height=12,
        entry=(0, 0),
        exit=(11, 11),
        output_file="example.txt",
        perfect=False
    )

    printer = AsciiPrinter()
    # old_printer = XAsciiPrinter()
    output = OutputGenerator()
    maze_generator = MazeGenerator(config)
    printer.toggle_path()
    maze = maze_generator.create()
    printer.print_maze(maze)
    for _ in range(5):
        printer.rotate_colours()
        maze = maze_generator.create()
        printer.print_maze(maze)

    # old_printer.print_maze(maze)

    # output.create_output_txt(maze, config)

    # when run for the second time seed is not reset so new maze is created
    # maze = maze_generator.create()
    # printer.print_maze(maze)
    # output.create_output_txt(maze, config)

    # for row in maze.grid:
    #     print(row)
    # print("FINAL")
    # print_maze(maze_e, config.height, config.width)
