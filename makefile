# ==============================
# A-Maze-ing Project Makefile
# ==============================

PYTHON = python3
PIP = $(PYTHON) -m pip
MAIN = a_maze_ing.py
VENV = maze_venv

# Default target
.DEFAULT_GOAL := run

install:
	python3 -m pip install -r requirements.txt

# Install dependencies in a local virtualenv
venv_install:
	python3 -m venv maze_venv
	maze_venv/bin/python3 -m pip install -r requirements.txt

# Install dependencies in the current Python environment - dangerous, use with caution
install_force:
	$(PYTHON) -m pip install --break-system-packages -r requirements.txt

# Run project
run:
	@$(PYTHON) $(MAIN) || true

# Debug mode (pdb)
debug:
	@$(PYTHON) -m pdb $(MAIN) || true

# Clean cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Lint (mandatory flags)
lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install install_current run debug clean lint

