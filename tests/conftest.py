"""Shared test fixtures and utilities."""

import pytest

def solved_grid(size: int):
    """Generate a valid solved Sudoku grid of the given size (9 or 16)."""
    block = int(size ** 0.5)
    return [[((r * block + r // block + c) % size) + 1 for c in range(size)] for r in range(size)]


@pytest.fixture
def solved_grid_9x9():
    """Fixture providing a solved 9x9 Sudoku grid."""
    return solved_grid(9)


@pytest.fixture
def solved_grid_16x16():
    """Fixture providing a solved 16x16 Sudoku grid."""
    return solved_grid(16)
