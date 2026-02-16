*This project has been created as part of the 42 curriculum by <sukerl>, <kimendon>.*

Description:

Instructions:
STEP1: Development Environment

```bash
# Create a virtual environment in your project folder
python3 -m venv venv

# Activate the virtual environment (Linux/Mac)
source venv/bin/activate

# Activate the virtual environment (Windows PowerShell)
venv\Scripts\Activate.ps1

# Upgrade pip
pip install --upgrade pip

# Install your package build tools
pip install setuptools wheel build

# Optional: install type stubs for static checks
pip install types-setuptools

# Install development dependencies
pip install pytest mypy flake8

#Build your package (creates dist/ directory and mazegen.egg-info)
python -m build

# Install the wheel
pip install dist/mazegen-1.0.0-py3-none-any.whl

# Try importing the wheel: this is atest to check if installed correctly
python  #this means you go inside python prompt now lookslike this: >>>

import mazegen
mazegen.__version__
# This should print "1.0.0"
from mazegen import MazeGenerator
# If nothing happens: no ERROR it's installed correctly"
#Then exit python when done:
exit()



```
STEP 2: Install MLX (Mac Only)
```bash
# Make sure your virtual environment is active
pip install mlx-2.2-py3-ubuntu-any.whl
# Note: MLX requires X11 (XQuartz) on Mac. If you don’t have it, download and install it from https://www.xquartz.org

```
STEP 3: Run Maze Generator
```bash
# Activate virtual environment if not already active
source venv/bin/activate

# Run the main script with your config file
python3 a_maze_ing.py config.txt
```



Instructions:
## Step 1: Development

It is recommended to use a Python virtual environment for development:

```bash
python3 -m venv venv
source venv/bin/activate
pip install pytest mypy flake8

## Step 2: Install MLX for MAC
```bash
pip install mlx-2.2-py3-ubuntu-any.whl


Resources:



Aditionally:
• The complete structure and format of your config file.
• The maze generation algorithm you chose.
• Why you chose this algorithm.
• What part of your code is reusable, and how.
• Your team and project management with:
◦ The roles of each team member.
◦ Your anticipated planning and how it evolved until the end
◦ What worked well and what could be improved
◦ Have you used any specific tools? Which ones?


#after venv here:
#open cmd (like typing bash)
cmd
.\.venv\Scripts\activate.bat

#then:
bash
pip install setuptools types-setuptools
