#!/usr/bin/env python3

from mazegen import MazeGenerator, Config
from sukerl_print_ascii import AsciiPrinter
from sukerl_create_output_txt import OutputGenerator
from gpt_maze_visualizer import print_maze

if __name__ == "__main__":
    print("=== Generate maze ===")
    config = Config(
        width=12,
        height=12,
        entry=(0, 0),
        exit=(11, 11),
        output_file="example.txt",
        perfect=True
    )
    maze_genertor = MazeGenerator(config)
    maze = maze_genertor.create()
    printer = AsciiPrinter()
    printer.toggle_path()
    printer.print_maze(maze)
    output = OutputGenerator()
    output.create_output_txt(maze, config)
    # for row in maze.grid:
    #     print(row)
    print("FINAL")
    # print_maze(maze, config.height, config.width)
