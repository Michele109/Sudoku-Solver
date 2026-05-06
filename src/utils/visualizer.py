try:
    from ..utils.validation import SUPPORTED_GRID_SIZES, validate_grid_size
except Exception:
    # Allow running this file directly (e.g. "python src/utils/visualizer.py")
    # by falling back to absolute import when package-relative import fails.
    from src.utils.validation import SUPPORTED_GRID_SIZES, validate_grid_size


def char_to_int(char: str):
    """ #tested
    Converts a character to its corresponding integer value for Sudoku.
    """
    if char == '0' or char == '.':
        return 0
    elif '1' <= char <= '9':
        return int(char)
    elif 'A' <= char <= 'G': # Assuming A=10, B=11, ..., G=16
        return ord(char) - ord('A') + 10
    return int(char)


def int_to_char(num: int):
    """ #tested
    Converts an integer value back to its character representation for Sudoku.
    """
    if num == 0:
        return '.'
    elif 1 <= num <= 9:
        return str(num)
    elif 10 <= num <= 16:
        return chr(num - 10 + ord('A'))
    return str(num)


def print_sudoku_grid(sudoku_str : str, GRID_SIZE: int):
    """ #tested
    Prints a Sudoku grid in a human-readable format. The input is a string representation of the Sudoku grid, where each character represents a cell (0 or '.' for empty cells).
    The GRID_SIZE parameter determines whether it's a 9x9 or 16x16 Sudoku.
    """
    validate_grid_size(GRID_SIZE)

    #check if the input string length matches the expected length for the given GRID_SIZE
    if len(sudoku_str) != GRID_SIZE * GRID_SIZE:
        raise ValueError(f"Input string length must be {GRID_SIZE * GRID_SIZE} for a {GRID_SIZE}x{GRID_SIZE} Sudoku.")

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


def prepare_grid_from_string(sudoku_str, GRID_SIZE):
    """
    Converts a string representation of a Sudoku grid into a 2D list (grid) of integers.
    The input string should have a length of GRID_SIZE * GRID_SIZE, where each character
    represents a cell in the Sudoku grid (0 or '.' for empty cells).
    """
    validate_grid_size(GRID_SIZE)

    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            char_val = sudoku_str[i * GRID_SIZE + j]
            row.append(char_to_int(char_val))
        grid.append(row)
    return grid