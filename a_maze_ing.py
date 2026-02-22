#!/usr/bin/env python3
"""
Command-line interface entry point for the A-Maze-ing application.

This module:
- Loads configuration from a file
- Generates a maze
- Displays it in ASCII format
- Provides an interactive CLI for regenerating and modifying display options
"""
from mazegen import MazeGenerator, Maze, Config, ConfigParser, ConfigFileError, MazeGeneratorError
from print_ascii import AsciiPrinter
from create_output_txt import OutputGenerator
import sys


def generate_maze(config: Config, maze_generator: MazeGenerator) -> Maze:
    """Generate a maze and write it to an output file.

    Use the ``MazeGenerator`` instance and then ``OutputGenerator``
    to save the generated maze to a text file defined in the
    configuration.

    Args:
        config (Config): Configuration object containing maze settings.
        maze_generator (MazeGenerator): Instance responsible for
            generating the maze structure.

    Returns:
        Maze: The generated maze instance.
    """
    maze = maze_generator.create_maze()
    output = OutputGenerator()
    output.create_output_txt(maze, config)
    return maze


def interact_with_user(
        maze: Maze,
        config: Config,
        maze_generator: MazeGenerator
) -> None:
    """Start an interactive CLI session for maze manipulation.

    Displays a menu allowing the user to:
        1. Re-generate a new maze
        2. Show or hide the shortest path
        3. Rotate maze colors
        4. Quit the application

    The function runs in a loop until the user selects the quit option.
    Invalid inputs are handled gracefully and prompt the user again.

    Args:
        maze (Maze): The current maze instance to interact with.
    """
    choices: dict[int, str] = {
        1: "Re-generate a new maze",
        2: "Show/Hide path from entry to exit",
        3: "Rotate maze colors",
        4: "Quit"
    }

    while True:
        print("=== A-Maze-ing ===")
        for num, info in choices.items():
            print(f"{num}. {info}")
        try:
            choice = int(input("Choice? (1-4): "))
        except ValueError:
            print("\nPlease enter a number between 1 and 4.\n")
            continue

        if choice == 1:
            maze = generate_maze(config, maze_generator)
        elif choice == 2:
            printer.toggle_path()
        elif choice == 3:
            printer.rotate_colours()
        elif choice == 4:
            break
        else:
            print("\nPlease enter a number between 1 and 4.\n")
            continue

        printer.print_maze(maze)


if __name__ == "__main__":
    args = len(sys.argv)
    if args != 2:
        print("Invalid number of arguments provided. Please enter 'python3 a_maze_ing.py config.txt")
    else:
        try:
            config = ConfigParser().load(sys.argv[1])
            maze_generator = MazeGenerator(config)
            maze = generate_maze(config, maze_generator)
            printer = AsciiPrinter()
            printer.print_maze(maze)
            interact_with_user(maze, config, maze_generator)
        except (ConfigFileError, MazeGeneratorError, OSError) as e:
            print(f"Error: {e}")
