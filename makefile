# ==============================
# A-Maze-ing Project Makefile
# ==============================

PYTHON = python3
PIP = pip3
MAIN = a_maze_ing.py

# Default target
.DEFAULT_GOAL := run

# Install dependencies
install:
	$(PIP) install -r requirements.txt --break-system-packages
	# 1. Create a virtual environment named 'venv'
	python3 -m venv venv
	# 2. Use the pip inside the venv to install your requirements
	./venv/bin/pip install -r requirements.txt

# Run project
run:
	./venv/bin/python a_maze_ing.py

# Debug mode (pdb)
debug:
	$(PYTHON) -m pdb $(MAIN)

# Clean cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Lint (mandatory flags)
lint:
	-python3 -m flake8 .
	-python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	
