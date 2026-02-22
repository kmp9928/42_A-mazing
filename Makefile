TO_RUN := a_maze_ing.py config.txt
VENV := .venv
# Detect the correct Python and pip executables inside the venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# If the Unix/macOS path doesn't exist, fallback to Windows-style
ifeq ("$(wildcard $(PYTHON))","")
	PYTHON := $(VENV)/Scripts/python
	PIP := $(VENV)/Scripts/pip
endif

.PHONY: help venv install run test lint lint-strict clean


help:
	@echo "Commands:"
	@echo "make venv			Installs virtual environment if not aleady present #, every other comand runs with ...: venv"
	@echo "make install			Installs development dependencies: mypy, flake8, pytest, pip(upgrade)"
	@echo "make run				runs a_maze_ing.py config.txt"
	@echo "make debug			runs your program in pdb"
	@echo "make lint			runs flake8 and mypy tests"
	@echo "make lint-strict		runs flake8 and mypy --strict"
	@echo "make clean			cleans pycache, dist,  build, *.egg-info"


venv:
ifeq ("$(wildcard $(VENV))","")
	@echo "Virtual environment not found. Creating $(VENV)..."
	@python -m venv $(VENV)
else
	@echo "Virtual environment already exists."
endif


install: venv
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install mypy flake8 pytest
	@echo "Dependencies installed"


run:
	@$(PYTHON) $(TO_RUN)


debug:
	@$(PYTHON) -m pdb $(TO_RUN)


lint:
	@$(PYTHON) -m flake8 .
	@$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs


lint-strict:
	@$(PYTHON) -m flake8 .
	@$(PYTHON) -m mypy . --strict	


clean:
# if OS equals Windows: cleaning syntax for Windows:
ifeq ($(OS),Windows_NT)
	@rmdir /s /q __pycache__ 2>nul || true
	@rmdir /s /q dist 2>nul || true
	@rmdir /s /q build 2>nul || true
	@del /q *.egg-info 2>nul || true
# Unix 
else
	@rm -rf __pycache__ dist build *.egg-info
endif
	@echo "Cleaned build artifacts and cache files"
