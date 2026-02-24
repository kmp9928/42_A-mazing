TO_RUN := a_maze_ing.py config.txt
VENV := .venv
# Detect the correct Python and pip executables inside the venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PACKAGE := mazegen-1.0.0.tar.gz
EXTRACT_DIR := mazegen-1.0.0
INCLUDE_FILES := \
				a_maze_ing.py \
				create_output_txt.py \
				print_ascii.py \
				render_maze.py

# If the Unix/macOS path doesn't exist, fallback to Windows-style
ifeq ("$(wildcard $(PYTHON))","")
	PYTHON := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip
endif

.PHONY: help venv install run test lint lint-strict clean debug unpack

help:
	@echo "Commands:"
	@echo "make install			Installs development dependencies: mypy, flake8, pytest, pip(upgrade) and mazegen"
	@echo "make run 			runs a_maze_ing.py config.txt"
	@echo "make debug			runs your program in pdb"
	@echo "make lint			runs flake8 and mypy tests"
	@echo "make lint-strict		runs flake8 and mypy --strict"
	@echo "make clean			cleans pycache, dist,  build, *.egg-info"


unpack:
ifeq ("$(wildcard $(EXTRACT_DIR))","")
	@echo "Extracting $(PACKAGE)..."
	tar -xzf $(PACKAGE)
else
	@echo "$(EXTRACT_DIR) already exists."
endif


install: unpack
ifeq ("$(wildcard $(VENV))","")
	@echo "Virtual environment not found. Creating $(VENV)..."
	@python -m venv $(VENV)
else
	@echo "Virtual environment already exists."
endif
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install mypy flake8 pytest
	@$(PYTHON) -m pip install ./$(EXTRACT_DIR)
	@echo "Dependencies and mazegen installed"


run:
	@$(PYTHON) $(TO_RUN)


debug:
	@$(PYTHON) -m pdb $(TO_RUN)


lint:
	@$(PYTHON) -m flake8 $(INCLUDE_FILES)
	@$(PYTHON) -m mypy \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs $(INCLUDE_FILES)


lint-strict:
	@$(PYTHON) -m flake8 $(INCLUDE_FILES)
	@$(PYTHON) -m mypy $(INCLUDE_FILES)


clean:
# if OS equals Windows: cleaning syntax for Windows:
ifeq ($(OS),Windows_NT)
	@rmdir /s /q __pycache__ 2>nul || true
	@rmdir /s /q dist 2>nul || true
	@rmdir /s /q build 2>nul || true
	@del /q *.egg-info 2>nul || true
# Unix 
else
	@rm -rf mazegen-1.0.0 __pycache__ .mypy_cache mazegen/__pycache__ dist build *.egg-info
endif
	@echo "Cleaned build artifacts and cache files"
