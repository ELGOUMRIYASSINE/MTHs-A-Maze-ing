# ==============================
# A-Maze-ing Project Makefile
# ==============================

PYTHON = python3
PIP = $(PYTHON) -m pip
MAIN = a_maze_ing.py

# Default target
.DEFAULT_GOAL := run

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Run project
run:
	@$(PYTHON) $(MAIN) || true

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
	-$(PYTHON) -m flake8 .
	-$(PYTHON) -m mypy . --explicit-package-bases --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint
	
