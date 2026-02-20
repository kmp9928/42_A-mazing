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


def create_maze(config: Config, maze_generator: MazeGenerator) -> Maze:
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


def draw_maze(maze: Maze, show_path: bool, rotate_colors: bool) -> None:
    """Render the maze in ASCII format.

    Optionally toggles display of the shortest path and rotates
    the color scheme before printing the maze.

    Args:
        maze (Maze): The maze to render.
        show_path (bool): If True, display the shortest path from
            entry to exit.
        rotate_colors (bool): If True, rotate the color scheme used
            for rendering.
    """
    printer = AsciiPrinter()
    if show_path:
        printer.toggle_path()
    if rotate_colors:
        printer.rotate_colours()
    printer.print_maze(maze)


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

    show_shortest_path = False
    rotate_colors = False
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
            maze = create_maze(config, maze_generator)
        elif choice == 2:
            show_shortest_path = not show_shortest_path
        elif choice == 3:
            rotate_colors = not rotate_colors
        elif choice == 4:
            break
        else:
            print("\nPlease enter a number between 1 and 4.\n")
            continue

        draw_maze(maze, show_shortest_path, rotate_colors)


if __name__ == "__main__":
    args = len(sys.argv)
    if args == 1:
        print("Configuration file missing. Please run again including it.")
    else:
        try:
            config = ConfigParser().load(sys.argv[1])
            maze_generator = MazeGenerator(config)
            maze = create_maze(config, maze_generator)
            draw_maze(maze, False, False)
            interact_with_user(maze, config, maze_generator)
        except (ConfigFileError, MazeGeneratorError) as e:
            print(f"Error: {e}")
