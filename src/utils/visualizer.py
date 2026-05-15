import math

from src.utils.validation import validate_grid_size
from src.utils.constants import char_to_int, int_to_char


def check_grid_size(sudoku_str: str, grid_size: int):
    """
    Validates that the provided grid size is supported (e.g., 9 or 16).
    Raises a ValueError if the grid size is not supported.
    """
    if not (sudoku_str and len(sudoku_str) == grid_size * grid_size):
        raise ValueError(f"Input string must have a length of {grid_size * grid_size}, got {len(sudoku_str)}")

def print_sudoku_grid(sudoku_str : str):
    """
    Prints a Sudoku grid in a human-readable format.
    The input is a string representation of the Sudoku grid, where each character represents a cell (0 or '.' for empty cells).
    """
    GRID_SIZE = int(math.isqrt(len(sudoku_str)))
    validate_grid_size(GRID_SIZE)

    check_grid_size(sudoku_str, GRID_SIZE)

    if GRID_SIZE == 16:

        grid = []
        # Convert string to 16x16 grid of integers
        for i in range(16):
            row = [char_to_int(sudoku_str[i*16 + j]) for j in range(16)]
            grid.append(row)

        for i in range(16):
            if i % 4 == 0 and i != 0:
                # Separator for 4x4 blocks
                print(f'{"-" * 40}')

            for j in range(16):
                if j % 4 == 0 and j != 0:
                    print(" | ", end="")

                # Print the character representation
                char_to_display = int_to_char(grid[i][j]) if grid[i][j] != 0 else "."
                if j == 15:
                    print(char_to_display)
                else:
                    print(char_to_display, end=" ")

    elif GRID_SIZE == 9:

        grid = []
        # Convert string to 9x9 grid of integers
        for i in range(9):
            row = [char_to_int(sudoku_str[i*9 + j]) for j in range(9)]
            grid.append(row)

        for i in range(9):
            if i % 3 == 0 and i != 0:
                # Separator for 3x3 blocks
                print(f"{'-' * 23}")

            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                # Print the character representation
                char_to_display = int_to_char(grid[i][j]) if grid[i][j] != 0 else "."
                if j == 8:
                    print(char_to_display)
                else:
                    print(char_to_display, end=" ")


def prepare_grid_from_string(sudoku_str: str) -> list:
    """
    Converts a string representation of a Sudoku grid into a 2D list (grid) of integers.
    The input string should have a length of GRID_SIZE * GRID_SIZE, where each character
    represents a cell in the Sudoku grid (0 or '.' for empty cells).
    """
    GRID_SIZE = int(math.isqrt(len(sudoku_str)))
    validate_grid_size(GRID_SIZE)

    check_grid_size(sudoku_str, GRID_SIZE)

    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            char_val = sudoku_str[i * GRID_SIZE + j]
            row.append(char_to_int(char_val))
        grid.append(row)
    return grid

def prepare_string_from_grid(grid: list) -> str:
    """
    Prepares a string representation of a Sudoku grid from a 2D list (grid) of integers.
    """
    #validating the grid shape (NxN), and that the grid size is supported
    GRID_SIZE = len(grid)
    validate_grid_size(GRID_SIZE)

    return "".join("".join(int_to_char(cell) for cell in row) for row in grid)