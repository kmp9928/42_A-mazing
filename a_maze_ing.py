#!/usr/bin/env python3

from mazegen import MazeGenerator, Maze, Config, ConfigParser, ConfigFileError, MazeGeneratorError
from print_ascii import AsciiPrinter
from create_output_txt import OutputGenerator
from gpt_maze_visualizer import print_maze
import sys


def create_maze(config: Config, maze_generator: MazeGenerator) -> Maze:
    maze = maze_generator.create_maze()
    output = OutputGenerator()
    output.create_output_txt(maze, config)
    return maze


def draw_maze(maze: Maze, show_path: bool, rotate_colors: bool) -> None:
    printer = AsciiPrinter()
    if show_path:
        printer.toggle_path()
    if rotate_colors:
        printer.rotate_colours()
    printer.print_maze(maze)


if __name__ == "__main__":
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
        draw_maze(maze, False, False)
        choices: dict[int, str] = {
            1: "Re-generate a new maze",
            2: "Show/Hide path from entry to exit",
            3: "Rotate maze colors",
            4: "Quit"
        }

        print("=== A-Maze-ing ===")

        show_shortest_path = False
        rotate_colors = False
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
                draw_maze(maze, show_shortest_path, rotate_colors)
            elif choice == 2:
                show_shortest_path = not show_shortest_path
                draw_maze(maze, show_shortest_path, rotate_colors)
            elif choice == 3:
                rotate_colors = not rotate_colors
                draw_maze(maze, show_shortest_path, rotate_colors)
            elif choice == 4:
                break
            else:
                print("\nPlease enter a number between 1 and 4.\n")
                continue
