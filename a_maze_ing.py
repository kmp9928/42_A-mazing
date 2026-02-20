#!/usr/bin/env python3

from mazegen import MazeGenerator, Maze, Config, ConfigParser, ConfigFileError, MazeGeneratorError
from sukerl_print_ascii import AsciiPrinter
from sukerl_create_output_txt import OutputGenerator
from gpt_maze_visualizer import print_maze
import sys


def create_maze(config: Config, maze_generator: MazeGenerator) -> Maze:
    maze = maze_generator.create_maze()
    output = OutputGenerator()
    output.create_output_txt(maze, config)
    return maze


def print_maze_path(maze: Maze, show_path: bool) -> None:
    printer = AsciiPrinter()
    printer.print_maze(maze)
    if not show_path:
        printer.toggle_path()


if __name__ == "__main__":
    #create config
    # create maze_gen
    #crete maze
    #ask on screen and action depedning on it
    
    # config = Config(
    #     width=50,
    #     height=40,
    #     entry=(0, 0),
    #     exit=(49, 39),
    #     output_file="output_maze.txt",
    #     perfect=False
    # )
    args = len(sys.argv)
    if args == 1:
        print("Configuration file missing. Please run again including it.")
    else:
        try:
            config = ConfigParser().load(sys.argv[1])
            maze_generator = MazeGenerator(config)
        except (ConfigFileError, MazeGeneratorError) as e:
            print(f"Error: {e}")

        maze = create_maze(config, maze_generator)
        print_maze_path(maze, False)
        choices: dict[int, str] = {
            1: "Re-generate a new maze",
            2: "Show/Hide path from entry to exit",
            3: "Rotate maze colors",
            4: "Quit"
        }

        print("=== A-Maze-ing ===")
        while True:
            for num, info in choices.items():
                print(f"{num}. {info}")
            try:
                choice = int(input("Choice? (1-4): "))
            except ValueError:
                print("\nPlease enter a number between 1 and 4.\n")
                continue

            if choice == 1:
                maze = create_maze(config, maze_generator)
                print_maze_path(maze, False)
            elif choice == 2:
                print_maze_path(maze, True)
            elif choice == 3:
                break
            elif choice == 4:
                break
            else:
                print("\nPlease enter a number between 1 and 4.\n")
                continue


        

    # maze_generator = MazeGenerator(config)

    # maze = maze_generator.create_maze()
    # printer.print_maze(maze)
    # output.create_output_txt(maze, config)

    # when run for the second time seed is not reset so new maze is created
    # maze = maze_generator.create()
    # printer.print_maze(maze)
    # output.create_output_txt(maze, config)

    # for row in maze.grid:
    #     print(row)
    # print("FINAL")
    # print_maze(maze, config.height, config.width)
