*This project has been created as part of the 42 curriculum by <sukerl>, <kimendon>.*

# --------------------------A-Maze-ing---------------------------------

## -------------------------Description--------------------------------
A-Maze-ing is a Python project that generates mazes based on a configurable input file: config.txt

The main goal of the project is to create a reusable maze generator module (`mazegen`) that can be installed via `pip` and used in other projects.  

Package (mazegen) provides:
- A MazeGenerator class for creating mazes of any size, with optional seeding for reproducibility.
- Access to the perfect path (shortest solution) for each maze.
- Validation of configuration files to ensure correct maze parameters (dimensions, entry/exit, correct type, missing keys etc.).

Main program provides:
- Generates the maze with help of the installed package.  
- ASCII visualization of the generated maze. 
- Writing each maze to an output text file using a compact hexadecimal format per cell, followed by the entry/exit coordinates and the shortest path.



## -------------------------Instructions-------------------------------


### 1. Setup Virtual Environment
Create a virtual environment for dependency isolation (recommended):  
```bash
make venv
```

### 2. Install Dependencies
Install all required development dependencies (mypy, flake8, pytest, pip upgrade):  
```bash
make install
```

### 3. Install the `mazegen` Package
```bash
# Install your package build tools
pip install setuptools wheel build

# Optional: install type stubs for static checks
pip install types-setuptools

#Build your package (creates dist/ directory and mazegen.egg-info)
python -m build

# Install the wheel
pip install dist/mazegen-1.0.0-py3-none-any.whl

# Optional: Test if Installation was successfull
# Try importing the wheel: this is a test to check if it installed correctly
python  #this means you go inside python prompt now lookslike this: >>>

import mazegen
mazegen.__version__
# This should print "1.0.0"
from mazegen import MazeGenerator
# If nothing happens: no ERROR it's installed correctly"
#Then exit python when done:
exit()
```

### 4. Run the Program
Install all required development dependencies (mypy, flake8, pytest, pip upgrade):  
```bash
make run
```
### 5. Other Available Options
The project includes a Makefile to simplify common tasks. Run the following command to see all available options: 
```bash
make help
make venv			# Installs virtual environment if not aleady present
make install		# Installs development dependencies: mypy, flake8, pytest, pip(upgrade)
make run			# runs a_maze_ing.py config.txt
make debug			# runs your program in pdb
make test			# runs test_config_parser.py
make lint			# runs flake8 and mypy tests
make lint-strict	# runs flake8 and mypy --strict
make clean			# cleans pycache, dist,  build, *.egg-info
```



## -------------------------Configuration File-------------------------
- The configuration file must contain one ‘KEY=VALUE‘ pair per line.
- Lines starting with # are comments and must be ignored.
- The following keys are mandatory: WIDTH, HEIGHT, ENTRY,EXIT, OUTPUT_FILE, PERFECT
- Optional keys: SEED

Example:

WIDTH=12
HEIGHT=12
ENTRY=0,0
EXIT=11,11
OUTPUT_FILE=example.txt
PERFECT=True
SEED=1



## -------------------------Maze Generation Algorithm------------------
The `mazegen` Package uses a Depth-First Search (DFS) backtracking algorithm to carve the maze:

- Starting from the entry point, it recursively visits unvisited neighboring cells, carving paths only if the cell has not been visited yet. This ensures that no loops are ever created.
- Dead ends are backtracked until the entire maze is fully explored.
- Supports a “perfect maze” mode by design, where all cells are reachable with a single unique path between any two points.


Why this algorithm was chosen:

- Simple to implement and understand while producing a complete, connected maze.
- Guarantees all cells are reachable and always creates a perfect maze with no loops.
- Easily extensible for adding custom features like fixed patterns (e.g., the “42” pattern).
- Provides full control over maze structure and reproducibility with a seed.
- Compared to other algorithms like Prim’s or Kruskal’s, DFS is:
    - Simpler and more straightforward to implement.
    - Naturally creates long, winding passages rather than many small isolated walls.
    - More memory-efficient for smaller mazes since it only needs a stack of visited paths, whereas Prim’s and Kruskal’s require managing edge lists or priority queues.



## -------------------------Reusable Code------------------------------
The maze generation logic is encapsulated in the MazeGenerator class, which is part of the standalone package `mazegen`.

What is reusable:
- The MazeGenerator class can be imported into any Python project and instantiated with custom parameters (width, height, entry, exit, perfect, seed).
- The configuration validation classes (Config and ConfigParser) are reusable for safely loading maze parameters from a configuration file.

Example:

from mazegen import MazeGenerator, Config

config = Config(
    width=12,
    height=12,
    entry=(0,0),
    exit=(11,11),
    output_file="example.txt",
    perfect=True
)

maze_gen = MazeGenerator(config, seed=1)
maze = maze_gen.create()



## -------------------------Team and Project Management----------------
- Team Roles:
    - Kimberly: Core maze generation, Configuration parser, Testing, 

    - Susanne: Package creation, Output formatting, ASCII display, Makefile, Documentation
- Planning & Evolution:
    - Initial planning focused on maze creation and validation
    - Adjustments made to implement “42” pattern and perfect mazes
    - Iterative testing with config files to ensure robustness
- What worked well / Improvements:
    - Modular design allowed isolated testing of maze generation
    - Future improvement: support multiple algorithms or visualization modes
- Tools Used:
    - Python 3.10+, venv, pip, make, flake8, mypy, pytest
    - AI assistance was used for brainstorming, subject explanations, code trouble shooting, structure and README drafting



## -------------------------References---------------------------------
### References
https://coderivers.org/blog/make-file-with-python/
https://www.w3schools.com/python/python_virtualenv.asp


### AI Assistance

AI was used as a supportive tool throughout the project for the following purposes:

- Explaining programming concepts and Python syntax relevant to the project.
- Troubleshooting and debugging code issues in modules and scripts.
- Providing guidance on project structure, packaging, and best practices.
- Drafting and refining documentation, including README content and usage instructions.
- Offering suggestions for implementing algorithms and designing reusable code components.

All code implementation, testing, and final decisions were performed manually by the team.
